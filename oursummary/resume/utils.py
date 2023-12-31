from django.urls import path


menu = [{'title': 'Главная страница', 'url_name': 'home'},
        {'title': 'Создать резюме', 'url_name': 'add_resume'},
        {'title': 'Мои Резюме', 'url_name': 'my_resumes'},
        {'title': 'Войти', 'url_name': 'home'},
        ]

card_filter = [{'filter': 'Earliest', 'title': 'Последние'},
               {'filter': 'Latest', 'title': 'Ранние'},
               {'filter': 'Experience', 'title': 'Есть опыт'},
               {'filter': 'Education', 'title': 'Есть образование'},
               {'filter': 'Drop', 'title': 'Сбросить'}]


class MenuMixin:
    def get_user_context(self, **kwargs):

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)
            user_menu.pop(1)

        context = kwargs
        context['menu'] = user_menu
        context['username'] = self.request.user.username
        context['card_filter'] = card_filter

        return context
