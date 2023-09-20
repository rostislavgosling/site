from django import forms
from transliterate import translit

from .models import *


class AddResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'letter', 'photo', 'is_shown']  # Поле Slug не включено, оно будет добавляться автоматически

