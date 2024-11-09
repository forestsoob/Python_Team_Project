# views.py
from django.shortcuts import render
from .models import Outfit, UserPreference, WeatherRecord
from django.conf import settings
from pyowm import OWM

def get_weather_data(city="Seoul"):
    owm = OWM(settings.WEATHER_API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    temperature = weather.temperature('celsius')["temp"]
    status = weather.detailed_status
    wind_speed = weather.wind()["speed"]  # 풍속
    humidity = weather.humidity  # 습도
    precipitation = weather.rain.get('1h', 0)  # 강수량 (1시간 기준)

    return {
        "temperature": temperature,
        "status": status,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "precipitation": precipitation
    }

def recommend_outfit(request):
    if request.user.is_authenticated:
        # 로그인된 사용자의 경우 UserPreference 불러오기
        user_pref, created = UserPreference.objects.get_or_create(user_id=request.user.id)
        avoid_categories = user_pref.avoid_categories.all()
    else:
        # 비로그인 사용자의 경우 기본 설정 사용
        avoid_categories = []  # 빈 리스트로 설정하여 오류 방지
    
    weather_data = get_weather_data()
    temperature = weather_data['temperature']
    conditions = weather_data['status']

    # 기온에 따른 기본 추천 Level
    warmth_level = 1 if temperature >= 30 else 2 if temperature >= 23 else 3 if temperature >= 15 else 4 if temperature >= 5 else 5
    
    # 특수 조건 적용 (비, 눈, 바람 등)
    if 'rain' in conditions.lower():
        warmth_level += 1
    elif 'snow' in conditions.lower():
        warmth_level += 2

    # 추천할 옷 필터링 (사용자가 피하고 싶은 종류 제외)
    exclude_ids = avoid_categories.values_list('id', flat=True) if hasattr(avoid_categories, 'values_list') else []
    recommended_outfits = Outfit.objects.filter(warmth_level=warmth_level).exclude(id__in=exclude_ids)
    
    return render(request, 'weather/recommendation.html', {
        'outfits': recommended_outfits,
        'temperature': temperature,
        'conditions': conditions,
        'wind_speed': weather_data["wind_speed"],
        'humidity': weather_data["humidity"],
        'precipitation': weather_data["precipitation"]
    })
