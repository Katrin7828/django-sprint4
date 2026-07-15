from django import forms
from .models import Congratulation


class CongratulationForm(forms.ModelForm):
    class Meta:
        model = Congratulation
        fields = ['text']
        widgets = {'text': forms.Textarea(attrs={'rows': 4,
                                                 'placeholder':
                                                 'Напишите поздравление автору'
                                                 'поста...',
                                                 'class': 'form-control'})}
        labels = {'text': ''}