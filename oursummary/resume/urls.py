from django.urls import path
from .views import *

urlpatterns = [
    path('<int:page>', Cards.as_view(), name='home'),
    path('resume/<slug:username>/<slug:resume_slug>', show_resume, name='resume'),
    path('addresume/', AddResume.as_view(), name='add_resume'),
    path('', redirect_to_main)
]
