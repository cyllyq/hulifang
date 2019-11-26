from django.contrib import admin
from .models import QuestionFeedback, UserMessage, ExamScore, DayScore


@admin.register(QuestionFeedback)
class QuestionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('question', 'user', 'comment', 'has_handle')
    search_filed = ('comment',)
    list_filter = ('has_handle',)
    list_editable = ('has_handle',)
    list_per_page = 20
    ordering = ('-create_time',)


@admin.register(ExamScore)
class ExamScore(admin.ModelAdmin):
    list_display = ('user', 'examination', 'score')
    search_filed = ('examination_name',)
    list_filter = ('examination',)
    list_per_page = 20
    ordering = ('-create_time',)


@admin.register(DayScore)
class DayScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'day_attendance', 'is_done')
    list_filter = ('day_attendance',)
    search_filed = ('day_attendance',)
    list_per_page = 20
    ordering = ('-create_time',)