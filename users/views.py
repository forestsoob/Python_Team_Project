from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile
from .forms import SignUpForm, LoginForm

# 회원가입 뷰
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)  # UserProfile 생성
            login(request, user)
            return redirect('home')  # 회원가입 후 홈으로 이동
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})

# 로그인 뷰
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

# 로그아웃 뷰
def logout_view(request):
    logout(request)
    return redirect('home')

# OOTD 사진 업로드 뷰
@login_required
def upload_ootd_view(request):
    if request.method == 'POST':
        photo = request.FILES.get('ootd_photo')
        profile = request.user.userprofile
        profile.ootd_photo = photo
        profile.save()
        messages.success(request, 'OOTD 사진이 업로드되었습니다.')
        return redirect('home')
    return render(request, 'upload_ootd.html')
