from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('weather/', include('weather.urls')),  
    path('users/', include('users.urls')),
    path('survey/', include('survey.urls')),
    path('', lambda request: redirect(reverse_lazy('recommend_outfit')), name='home'),  
]
