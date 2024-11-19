from django import forms
from .models import Feedback, OOTD

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['satisfaction']
        widgets = {
            'satisfaction': forms.RadioSelect(choices=[
                (1, '😢'),
                (2, '😐'),
                (3, '😊'),
            ]),
        }

class OOTDForm(forms.ModelForm):
    class Meta:
        model = OOTD
        fields = ['image']
