from django.urls import path
from .views import *

urlpatterns = [
    path('<int:page>', Cards.as_view(), name='home'),
    path('resume/<slug:resume_slug>', ShowResume.as_view(), name='resume'),
    path('addresume/', AddResume.as_view(), name='add_resume'),
    path('addeducation/<slug:resume_slug>', AddEducation.as_view(), name='add_education'),
    path('addexperience/<slug:resume_slug>', AddExperience.as_view(), name='add_experience'),
    path('myresumes/', MyResumes.as_view(), name='my_resumes'),
    path('', redirect_to_main, name='init'),
    path('<slug:resume_slug>/update', ResumeUpdate.as_view(), name='update_resume'),
    path('<int:pk>/deleteEd', DeleteEducation.as_view(), name='delete_education'),
    path('<int:pk>/deleteEx', DeleteExperience.as_view(), name='delete_experience'),
]
