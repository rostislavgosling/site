from django.urls import path


menu = [{'title': 'Главная страница', 'url_name': 'home'},
        {'title': 'Создать резюме', 'url_name': 'add_resume'},
        {'title': 'Мои Резюме', 'url_name': 'my_resumes'},
        {'title': 'Войти', 'url_name': 'home'},
        ]


class MenuMixin:

    def get_user_context(self, **kwargs):

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)

        context = kwargs
        context['menu'] = user_menu
        context['username'] = self.request.user.username

        return context
