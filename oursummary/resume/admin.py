from django.contrib import admin
from .models import *
# Register your models here.


class ResumeAdmin(admin.ModelAdmin):

    list_display = ('id', 'title', 'letter', 'time_created', 'is_shown')
    ist_display_links = ('id', 'title')


admin.site.register(Resume, ResumeAdmin)
admin.site.register(Education)
admin.site.register(Experience)