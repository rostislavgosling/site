from django.urls import path
from .views import *

urlpatterns = [
    path('<int:page>', Cards.as_view(), name='home'),
    path('resume/<slug:resume_slug>', ShowResume.as_view(), name='resume'),
    path('addresume/', AddResume.as_view(), name='add_resume'),
    path('addeducation/<slug:resume_slug>', AddEducation.as_view(), name='add_education'),
    path('<slug:username>', MyResumes.as_view(), name='my_resumes'),
    path('', redirect_to_main, name='init')
]
