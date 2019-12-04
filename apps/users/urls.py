from django.urls import path
from . import views


app_name = 'users'
urlpatterns = [
    path('wrongquestions', views.wrong_questions, name='wrong_questions'),
]