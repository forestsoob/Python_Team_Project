from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from weather.models import Outfit
from .models import Dislike

@login_required
def dislike_survey(request):
    if request.method == 'POST':
        disliked_outfits = request.POST.getlist('dislike')
        for outfit_id in disliked_outfits:
            outfit = Outfit.objects.get(id=outfit_id)
            Dislike.objects.get_or_create(user=request.user, outfit=outfit)
        return redirect('home')  # 홈 페이지로 리디렉션

    outfits = Outfit.objects.all()
    return render(request, 'survey/dislike_survey.html', {'outfits': outfits})