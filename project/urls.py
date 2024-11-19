from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings  # 추가
from django.conf.urls.static import static
from .views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),  
    path('users/', include('users.urls')),
    path('survey/', include('survey.urls')),
    path('feedback/', include('feedback.urls')),
    path('', home_view, name='home'),  # 초기화면을 홈 화면 뷰로 변경
]

# 미디어 파일 제공 설정 (DEBUG=True 환경에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)