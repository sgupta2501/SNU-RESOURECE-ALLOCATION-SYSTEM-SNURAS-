#from django.contrib import admin
from django.urls import include, path
from . import views

from .views import(
    register_teacher,
    register_student,
    #signup_teacher,
    #signup_student,
)

urlpatterns = [
    path('register_student/', views.register_student, name='register_student'),
    path('register_teacher/', views.register_teacher, name='register_teacher'),
    #path('signup_student/', views.signup_student, name='signup_student'),
    #path('signup_teacher/', views.signup_teacher, name='signup_teacher'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]