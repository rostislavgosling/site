menu = [{'title': 'Главная страница', 'url_name': 'home'},
        {'title': 'Создать резюме', 'url_name': 'home'},
        {'title': 'Войти', 'url_name': 'home'},
        ]


class MenuMixin:

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = menu

        return context
