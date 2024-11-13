from django import forms

class FeedbackForm(forms.Form):
    feedback_choices = [
        ('positive', '좋았다'),
        ('negative', '나쁘다')
    ]
    
    feedback = forms.ChoiceField(choices=feedback_choices, widget=forms.RadioSelect, label="옷에 대한 피드백")