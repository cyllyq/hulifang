from django.contrib import admin
from .models import Question, Chapter, Section, Examination, DayAttendance, SectionQuestion, DayQuestion, ExamQuestion


class SectionQuestionInline(admin.TabularInline):
    model = SectionQuestion
    extra = 1


class DayQuestionInline(admin.TabularInline):
    model = DayQuestion
    extra = 1


class ExamQuestionInline(admin.TabularInline):
    model = ExamQuestion
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'get_sections_count')
    search_fields = ('name', )
    list_per_page = 20
    ordering = ('number',)

    def get_sections_count(self, obj):
        return obj.sections.count()
    get_sections_count.short_description = u'节数'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'chapter', 'number', 'difficulty', 'is_keypoint', 'get_questions_count')
    search_fields = ('name', 'chapter__name')
    list_editable = ('is_keypoint', 'difficulty')
    list_filter = ('chapter__name', 'difficulty', 'is_keypoint')
    inlines = (SectionQuestionInline, )
    #raw_id_fields = ('chapter', )
    list_per_page = 20
    ordering = ('chapter__number', 'number')

    def get_questions_count(self, obj):
        return obj.questions.count()
    get_questions_count.short_description = u'题数'


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'exam_type', 'exam_time', 'get_questions_count')
    search_fields = ('name', 'exam_type')
    list_editable = ('exam_type', )
    list_filter = ('exam_type', )
    inlines = (ExamQuestionInline,)
    list_per_page = 20
    ordering = ('number',)

    def get_questions_count(self, obj):
        return obj.questions.count()
    get_questions_count.short_description = u'题数'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('stem', 'title', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'choice_e',
        'answer', 'analysis', 'image', 'video', 'question_type')
    search_fields = ('stem', 'title', )
    list_editable = ('answer', 'question_type')
    list_filter = ('question_type',)
    list_per_page = 20
    ordering = ('id',)


@admin.register(DayAttendance)
class DayAttendanceAdmin(admin.ModelAdmin):
    list_display = ('create_time', 'analysis_file')
    search_fields = ('create_time',)
    list_filter = ('create_time',)
    inlines = (DayQuestionInline, )
    list_per_page = 20
    ordering = ('-create_time',)