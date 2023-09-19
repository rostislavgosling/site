from django import template

register = template.Library()


@register.inclusion_tag('resume/user_card.html')
def show_user_card(info):
    return {'resume': info}


@register.inclusion_tag('resume/sidebar.html')
def show_sidebar(sidebar_info=None):
    return {'sidebar': sidebar_info}
