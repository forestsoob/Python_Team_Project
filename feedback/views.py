from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from weather.views import get_weather_data
from .models import Feedback, OOTD
from .forms import FeedbackForm, OOTDForm

@login_required
def feedback_view(request):
    feedback_form = FeedbackForm()
    ootd_form = OOTDForm()
    weather_data = get_weather_data("Seoul")  # 서울의 날씨 데이터를 가져옴

    if request.method == 'POST':
        if 'submit_feedback' in request.POST:
            feedback_form = FeedbackForm(request.POST)
            if feedback_form.is_valid():
                feedback = feedback_form.save(commit=False)
                feedback.user = request.user
                feedback.save()
                messages.success(request, "피드백이 제출되었습니다!")
                return redirect('feedback')

        if 'upload_ootd' in request.POST:
            ootd_form = OOTDForm(request.POST, request.FILES)
            if ootd_form.is_valid():
                ootd = ootd_form.save(commit=False)
                ootd.user = request.user
                ootd.save()
                messages.success(request, "OOTD 사진이 업로드되었습니다!")
                return redirect('feedback')

    return render(request, 'feedback/feedback.html', {
        'feedback_form': feedback_form,
        'ootd_form': ootd_form,
        'weather': weather_data  # 날씨 데이터를 템플릿에 전달
    })
