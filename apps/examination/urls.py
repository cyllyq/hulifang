from django.urls import path
from . import views


app_name = 'examination'
urlpatterns = [
    path('', views.section_list, name='section_list'),
    path('section/<int:section_id>', views.section_questions, name='section_questions'),
    path('examination', views.exam_list, name='exam_list'),
    path('examination/<int:exam_id>', views.examination, name='examination'),
    path('dayattendance', views.dayattendance, name='dayattendance'),
    path('question/addwrong/<int:question_id>', views.add_wrong_question, name='add_wrong_question')
    #path('wrong', views.wrong_questions, name='wrong_questions'), 移动用户模块中
]