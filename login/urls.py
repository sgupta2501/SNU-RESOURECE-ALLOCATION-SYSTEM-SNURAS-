from django.urls import include, path
from . import views
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import re_path as url
from django.contrib import admin
from django.views.generic import TemplateView


from .views import(
	group_check,
	logout_view,
	#register_teacher,
	#register_student,
	)

urlpatterns = [
      path('', LoginView.as_view(template_name='index.html'), name="home"),
      path('logout/', views.logout_view, name='logout'),
      path('group/', views.group_check, name='group'),
      #path('register_teacher/', TemplateView.as_view(template_name="register_teacher.html")),
      #path('register_student/', TemplateView.as_view(template_name="register_student.html")),
      #path('register_teacher/', register_teacher.as_view, name='register_teacher'),
      path('',include('authentication.urls')),
      #path('register_student/', views.register_student, name='register_student'),
      #path('register_teacher/', views.register_teacher, name='register_teacher'),
]

