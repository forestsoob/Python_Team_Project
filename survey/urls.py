from django.urls import path
from . import views

urlpatterns = [
    path('dislike-survey/', views.dislike_survey, name='dislike_survey'),
]
