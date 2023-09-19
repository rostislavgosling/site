from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from .utils import *
from .models import *


class Cards(MenuMixin, ListView):
    model = Resume
    template_name = 'resume/index.html'
    context_object_name = 'resumes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница", sidebar=True)
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Resume.objects.all()


def show_resume(request, username, resume_slug):
    return HttpResponse(f'<h2>Резюме {username} номер {resume_slug}</h2>')