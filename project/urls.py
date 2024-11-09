# project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),  # weather 앱의 URL 포함
    path('', lambda request: redirect('recommend_outfit')),  # 기본 경로 리디렉션
]
