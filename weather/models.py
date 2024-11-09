from django.db import models

class Outfit(models.Model):
    CATEGORY_CHOICES = [
        ('outer', '아우터'),
        ('top', '상의'),
        ('bottom', '하의'),
        ('other', '기타'),
    ]
    WARMTH_LEVEL_CHOICES = [
        (1, 'Level 1: 매우 더운 날씨 (30°C 이상)'),
        (2, 'Level 2: 더운 날씨 (23°C ~ 29°C)'),
        (3, 'Level 3: 선선한 날씨 (15°C ~ 22°C)'),
        (4, 'Level 4: 쌀쌀한 날씨 (5°C ~ 14°C)'),
        (5, 'Level 5: 매우 추운 날씨 (0°C 이하)'),
    ]
    
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    warmth_level = models.IntegerField(choices=WARMTH_LEVEL_CHOICES)
    is_frequent = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.name} (Level {self.warmth_level})"

class UserPreference(models.Model):
    user_id = models.IntegerField()  # 사용자 ID
    avoid_categories = models.ManyToManyField(Outfit, related_name="avoided_outfits")  # 사용자가 피하고 싶은 옷 종류
    temperature_feedback = models.JSONField(default=dict)  # 특정 기온에 대한 후기 저장
    condition_preference = models.CharField(max_length=20, default="normal")  # 컨디션 (e.g., 'unwell', 'active')

class WeatherRecord(models.Model):
    date = models.DateField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    wind_speed = models.FloatField()
    special_conditions = models.CharField(max_length=50, blank=True)  # 비, 눈 등
    user_outfit = models.ForeignKey(Outfit, on_delete=models.SET_NULL, null=True)  # OOTD
    feedback = models.CharField(max_length=20, blank=True)  # "추웠다" 등의 사용자 피드백


# 위치 기반 시스템 추가
# 기능 분류 및 html 작업