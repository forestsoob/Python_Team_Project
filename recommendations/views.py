from django.shortcuts import render, redirect
from .models import Outfit, UserPreference, WeatherRecord
from .forms import FeedbackForm
from django.conf import settings
from pyowm import OWM

# 날씨 데이터를 가져오는 함수
def get_weather_data(city="Seoul"):
    owm = OWM(settings.WEATHER_API_KEY)
    mgr = owm.weather_manager()
    observation = mgr.weather_at_place(city)
    weather = observation.weather
    temperature = weather.temperature('celsius')["temp"]
    status = weather.detailed_status
    wind_speed = weather.wind()["speed"]
    humidity = weather.humidity
    precipitation = weather.rain.get('1h', 0)

    return {
        "temperature": temperature,
        "status": status,
        "wind_speed": wind_speed,
        "humidity": humidity,
        "precipitation": precipitation
    }

# 추천 로직 (옷 추천과 피드백 처리)
def recommend_outfit(request):
    if request.user.is_authenticated:
        user_pref, created = UserPreference.objects.get_or_create(user_id=request.user.id)
        avoid_categories = user_pref.avoid_categories.all()
    else:
        avoid_categories = []  # 비로그인 사용자는 기본 설정으로 빈 리스트

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
    
    # 피드백 폼 처리
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            
            # 피드백에 따른 가중치 조정
            for outfit in recommended_outfits:
                # WeatherRecord를 통해 해당 옷에 대한 피드백 기록
                weather_record, created = WeatherRecord.objects.get_or_create(user_outfit=outfit)
                
                # 피드백에 따라 가중치 변경
                if feedback == 'negative':
                    # 부정적 피드백을 받았다면 가중치를 1단계 낮춤
                    if outfit.warmth_level > 1:
                        outfit.warmth_level -= 1
                    outfit.save()  # 가중치 업데이트 후 저장
                # 피드백을 받은 후, 사용자 피드백을 WeatherRecord에 기록
                weather_record.feedback = feedback
                weather_record.save()

            return redirect('recommend_outfit')  # 피드백을 제출하고 나면 다시 추천 페이지로 리디렉션

    else:
        form = FeedbackForm()

    # 추천된 옷들을 템플릿에 전달
    return render(request, 'weather/recommendation.html', {
        'outfits': recommended_outfits,
        'temperature': temperature,
        'conditions': conditions,
        'wind_speed': weather_data["wind_speed"],
        'humidity': weather_data["humidity"],
        'precipitation': weather_data["precipitation"],
        'form': form
    })
