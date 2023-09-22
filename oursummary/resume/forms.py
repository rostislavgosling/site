from datetime import datetime, date

from django import forms
from django.core.exceptions import ValidationError
from transliterate import translit

from .models import *


class AddResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['title', 'letter', 'photo', 'is_shown']  # Поле Slug не включено, оно будет добавляться автоматически


class AddEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['title', 'year_start', 'year_end',
                  'specialization']  # Поле Slug не включено, оно будет добавляться автоматически

        widgets = {'year_start': forms.SelectDateWidget(years=range(1950, 2030)),
                   'year_end': forms.SelectDateWidget(years=range(1950, 2030))
                   }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year_start'].initial = '2000-01-01'
        self.fields['year_end'].initial = '2000-01-01'

    def clean_year_start(self):
        year_s = self.cleaned_data['year_start']
        if year_s > date.today():
            raise ValidationError('Дата не может превышать текущий год')
        return year_s

    def clean_year_end(self):
        year_e = self.cleaned_data['year_end']
        if 'year_start' in self.cleaned_data:
            year_s = self.cleaned_data['year_start']
            year_e = self.cleaned_data['year_end']
            if year_e < year_s:
                raise ValidationError('Год окончания не может быть меньше года начала обучения')
        return year_e



class AddExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'date_start', 'date_end',
                  'post']  # Поле Slug не включено, оно будет добавляться автоматически
