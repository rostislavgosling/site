from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from .utils import *
from .models import *
from .forms import *
from transliterate import translit
import uuid


def redirect_to_main(request):
    return redirect('home', page=1)


def create_unique_url(user_input):
    # Генерируем уникальный идентификатор
    unique_id = str(uuid.uuid4().hex)[:3]  # Выбираем первые 10 символов из хеша
    return f"{user_input}-{unique_id}"


class Cards(MenuMixin, ListView):
    """
    Класс отображает карточки резюме по 6 на страницу
    В контекст передается ренж всех страниц для формирования списка номеров страниц на темплейте
    Сет резюме выбирается в зависимости от страницы пачками по 6
    """
    model = Resume
    template_name = 'resume/index.html'
    context_object_name = 'resumes'
    cards_on_page = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница",
                                      sidebar=True,
                                      all_pages=range(Resume.objects.all().count() // self.cards_on_page + 1))
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        page = self.kwargs.get('page')
        return Resume.objects.all()[self.cards_on_page * (page - 1):self.cards_on_page * page]


class ShowResume(MenuMixin, DetailView):
    """
    Класс отображает одно резюме
    """
    model = Resume
    template_name = 'resume/show.html'
    context_object_name = 'resume'
    slug_url_kwarg = 'resume_slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Резюме",
                                      sidebar=False,
                                      )
        return dict(list(context.items()) + list(c_def.items()))


class AddResume(LoginRequiredMixin, MenuMixin, CreateView):
    """
    Класс создает форму для заполнения резюме
    В контекст передаются url на который будет отправлена форма
    При валидности формы, формируется уникальный url и резюме привязывается к пользователю
    """
    model = Resume
    form_class = AddResumeForm
    template_name = 'resume/add_resume.html'
    login_url = reverse_lazy('home', kwargs={'page': 1})
    title_to_redirect = None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление резюме",
                                      sidebar=False,
                                      arg=None,
                                      url='add_resume',
                                      )
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # Извлекаем тайтл для преобразования в url
        title_to_convert = form.cleaned_data['title'].replace(' ', '').lower()

        # Создаем объект класса формы
        resume_form = form.save(commit=False)
        # Преобразуем тайтл в url с помощью транслита
        translit_title = translit(title_to_convert, 'ru', reversed=True)
        unique_url = create_unique_url(f'{self.request.user.username}-{translit_title}')
        resume_form.slug = unique_url
        self.success_url = reverse_lazy('add_education',
                                        kwargs={'resume_slug': unique_url})
        # Привязываем резюме к юзеру
        resume_form.user = User.objects.get(username=self.request.user.username)

        return super().form_valid(form)


class AddEducation(MenuMixin, CreateView):
    model = Education
    form_class = AddEducationForm
    template_name = 'resume/add_resume.html'
    login_url = reverse_lazy('home', kwargs={'page': 1})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление образования",
                                      sidebar=False,
                                      arg=self.kwargs.get('resume_slug'),
                                      url='add_education'
                                      )
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        # Создаем объект класса формы
        edc_form = form.save(commit=False)
        # Добавляем ключ для Resume элемента
        edc_form.resume = Resume.objects.get(slug=self.kwargs.get('resume_slug'))
        return super().form_valid(form)


# class AddExperience(MenuMixin, CreateView):
#     model = Experience
#     form_class = AddExperienceForm
#     template_name = 'resume/add_resume.html'
#     login_url = reverse_lazy('home', kwargs={'page': 1})
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title="Добавление образования",
#                                       sidebar=False,
#                                       arg=self.kwargs.get('resume_slug'),
#                                       url='add_education'
#                                       )
#         return dict(list(context.items()) + list(c_def.items()))
#
#     def form_valid(self, form):
#         # Создаем объект класса формы
#         edc_form = form.save(commit=False)
#         # Добавляем ключ для Resume элемента
#         edc_form.resume = Resume.objects.get(slug=self.kwargs.get('resume_slug'))
#         return super().form_valid(form)
#

class MyResumes(LoginRequiredMixin, MenuMixin, ListView):
    """
    Класс отображения личного кабинета пользователя
    """
    model = Resume
    template_name = 'resume/my_resumes.html'
    login_url = reverse_lazy('home', kwargs={'page': 1})
    context_object_name = 'resumes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Мои резюме",
                                      sidebar=False,
                                      )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Resume.objects.filter(user=User.objects.get(username=self.request.user.username))
