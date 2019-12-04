from django.contrib import admin
from .models import Question, Chapter, Section, Examination, DayAttendance, SectionQuestion, DayQuestion, ExamQuestion
from django.urls import reverse
from django.utils.html import format_html


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'get_sections_count')
    search_fields = ('name', )
    list_per_page = 20
    ordering = ('number',)

    def get_sections_count(self, obj):
        return format_html('<a target="_blank" href="{}">{} 查看节</a>'.format(
            reverse('admin:examination_section_changelist')+'?chapter__id={}'.format(obj.id), str(obj.sections.count())))
    get_sections_count.short_description = u'节数'


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):

    class SectionQuestionInline(admin.TabularInline):
        model = SectionQuestion
        extra = 1


    list_display = ('name', 'chapter', 'number', 'difficulty', 'is_keypoint', 'get_questions_count')
    search_fields = ('name', 'chapter__name')
    list_editable = ('is_keypoint', 'difficulty')
    list_filter = ('chapter__name', 'difficulty', 'is_keypoint',)
    #inlines = (SectionQuestionInline, )
    #raw_id_fields = ('chapter', )
    list_per_page = 20
    ordering = ('chapter__number', 'number')

    def get_questions_count(self, obj):
        return format_html('<a target="_blank" href="{}">{} 查看题目</a>'.format(
            reverse('admin:examination_sectionquestion_changelist')+'?section__id={}'.format(obj.id), str(obj.questions.count())))
    get_questions_count.short_description = u'题数'


@admin.register(Examination)
class ExaminationAdmin(admin.ModelAdmin):

    class ExamQuestionInline(admin.TabularInline):
        model = ExamQuestion
        extra = 1

    list_display = ('name', 'number', 'exam_type', 'exam_time', 'get_questions_count')
    search_fields = ('name', 'exam_type')
    list_editable = ('exam_type', )
    list_filter = ('exam_type', )
    #inlines = (ExamQuestionInline,)
    list_per_page = 20
    ordering = ('number',)

    def get_questions_count(self, obj):
        return format_html('<a target="_blank" href="{}">{} 查看题目</a>'.format(
            reverse('admin:examination_examquestion_changelist')+'?examination__id={}'.format(obj.id), str(obj.questions.count())))
    get_questions_count.short_description = u'题数'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('stem', 'title', 'choice_a', 'choice_b', 'choice_c', 'choice_d', 'choice_e',
        'answer', 'analysis', 'image', 'video', 'question_type')
    list_display_links = ('stem', 'title')
    search_fields = ('stem', 'title', )
    list_editable = ('answer', 'question_type')
    list_filter = ('question_type',)
    list_per_page = 20
    ordering = ('id',)

    # actions = ['export_excel']

    # def export_excel(self, request, queryset):
    #     pass

    # export_excel.short_description = '导入'
    # export_excel.icon = 'fas fa-audio-description'
    # export_excel.type = 'danger'
    

    # def lookup_allowed(self, key, value):
    #     if key in ('examquestion__examination__id', ):
    #         return True
    #     return super(QuestionAdmin, self).lookup_allowed(key, value)



@admin.register(DayAttendance)
class DayAttendanceAdmin(admin.ModelAdmin):

    class DayQuestionInline(admin.TabularInline):
        model = DayQuestion
        extra = 1

    list_display = ('create_time', 'analysis_file', 'get_questions')
    search_fields = ('create_time',)
    list_filter = ('create_time',)
    #inlines = (DayQuestionInline, )
    list_per_page = 20
    ordering = ('-create_time',)

    def get_questions(self, obj):
        return format_html('<a target="_blank" href="{}">查看题目</a>'.format(
            reverse('admin:examination_dayquestion_changelist')+'?dayattendance__id__exact={}'.format(obj.id)))
    get_questions.short_description = u'题目'


@admin.register(SectionQuestion)
class SectionQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_section_name', 'get_question_stem', 'get_question_title', 'number', 'change_question',)
    search_fields = ('question__name', 'section__name')
    list_filter = ('section__name', )
    list_display_links = ('get_question_stem', 'get_question_title', 'get_section_name')
    list_editable = ('number',)
    list_per_page = 20
    ordering = ('section__id', 'number')
    raw_id_fields = ('question', )
    #autocomplete_fields = ('question', )

    #该方法返回空,可不在菜单栏显示
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_question_stem(self, obj):
        return obj.question.stem
    get_question_stem.short_description = '题干'

    def get_question_title(self, obj):
        return obj.question.title
    get_question_title.short_description = '题目'

    def get_section_name(self, obj):
        return obj.section.name
    get_section_name.short_description = '所属章节'

    def change_question(self, obj):
        return format_html('<a class="related-widget-wrapper-link change-related" href="{}">修改题目</a>'.format(
            reverse('admin:examination_question_change', args=(obj.question.id,))))
    change_question.short_description = '修改题目'


@admin.register(ExamQuestion)
class ExamQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_exam_name', 'get_question_stem', 'get_question_title', 'number', 'change_question',)
    search_fields = ('question__name', 'examination__name')
    list_filter = ('examination', )
    list_display_links = ('get_question_stem', 'get_question_title', 'get_exam_name')
    list_editable = ('number',)
    list_per_page = 20
    ordering = ('examination__id', 'number')
    raw_id_fields = ('question', )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_question_stem(self, obj):
        return obj.question.stem
    get_question_stem.short_description = '题干'

    def get_question_title(self, obj):
        return obj.question.title
    get_question_title.short_description = '题目'

    def get_exam_name(self, obj):
        return obj.examination.name
    get_exam_name.short_description = '所属试卷'

    def change_question(self, obj):
        return format_html('<a class="related-widget-wrapper-link change-related" href="{}">修改题目</a>'.format(
            reverse('admin:examination_question_change', args=(obj.question.id,))))
    change_question.short_description = '修改题目'


@admin.register(DayQuestion)
class DayQuestionAdmin(admin.ModelAdmin):
    list_display = ('get_day_name', 'get_question_stem', 'get_question_title', 'number', 'change_question',)
    search_fields = ('question__name', 'day_attendance__create_time')
    list_filter = ('day_attendance__create_time', )
    list_display_links = ('get_question_stem', 'get_question_title', 'get_day_name')
    list_editable = ('number',)
    list_per_page = 20
    ordering = ('day_attendance__id', 'number')
    raw_id_fields = ('question', )

    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}

    def get_question_stem(self, obj):
        return obj.question.stem
    get_question_stem.short_description = '题干'

    def get_question_title(self, obj):
        return obj.question.title
    get_question_title.short_description = '题目'

    def get_day_name(self, obj):
        return '每日打卡' + str(obj.day_attendance.create_time)
    get_day_name.short_description = '每日打卡'

    def change_question(self, obj):
        return format_html('<a class="related-widget-wrapper-link change-related" href="{}">修改题目</a>'.format(
            reverse('admin:examination_question_change', args=(obj.question.id,))))
    change_question.short_description = '修改题目'