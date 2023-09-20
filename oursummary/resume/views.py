from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from .utils import *
from .models import *
from .forms import *
from transliterate import translit


class Cards(MenuMixin, ListView):
    model = Resume
    template_name = 'resume/index.html'
    context_object_name = 'resumes'
    cards_on_page = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница",
                                      sidebar=True,
                                      all_pages=range(Resume.objects.all().count() // self.cards_on_page + 1))
        print(range(Resume.objects.all().count() // self.cards_on_page))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        page = self.kwargs.get('page')
        return Resume.objects.all()[self.cards_on_page * (page - 1):self.cards_on_page * page]


def show_resume(request, username, resume_slug):
    return HttpResponse(f'<h2>Резюме {username} номер {resume_slug}</h2>')


# Форма для заполнения резюме
class AddResume(MenuMixin, CreateView):
    model = Resume
    form_class = AddResumeForm
    template_name = 'resume/add_resume.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление резюме", sidebar=False)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # Извлекаем тайтл для преобразования в url
        title_to_convert = form.cleaned_data['title'].replace(' ', '').lower()
        # Создаем объект класса формы
        resume_form = form.save(commit=False)
        # Преобразуем тайтл в url с помощью транслита
        translit_title = translit(title_to_convert, 'ru', reversed=True)

        resume_form.slug = translit_title

        return super().form_valid(form)


def redirect_to_main(request):
    return redirect('home', page=1)

