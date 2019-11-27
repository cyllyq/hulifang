from django.db import models
from abstract import QuestionModel, DelModel, TimeModel


class Question(models.Model):
    TYPE_CHOICE = (
        (0, '单选题'),
        (1, '多选题'),
        (2, '判断题'),
    )

    question_type = models.PositiveIntegerField(default=0, choices=TYPE_CHOICE, verbose_name='题目类型')
    title = models.CharField(db_index=True, max_length=200, verbose_name=u'题目')
    stem = models.CharField(db_index=True, max_length=200, null=True, blank=True, verbose_name=u'题干')
    #number = models.IntegerField(verbose_name=u'序号')
    answer = models.CharField(max_length=1, verbose_name=u'答案')
    analysis = models.CharField(max_length=500, verbose_name=u'解析')
    choice_a = models.CharField(max_length=100, verbose_name=u'选项A')
    choice_b = models.CharField(max_length=100, verbose_name=u'选项B')
    choice_c = models.CharField(max_length=100, verbose_name=u'选项C')
    choice_d = models.CharField(max_length=100, verbose_name=u'选项D')
    choice_e = models.CharField(max_length=100, verbose_name=u'选项E')
    image = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'图片')
    video = models.CharField(max_length=100, null=True, blank=True, verbose_name=u'视频')

    class Meta:
        verbose_name = '题目库'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title



class Chapter(TimeModel):
    name = models.CharField(max_length=100, db_index=True, verbose_name=u'章名称')
    number = models.IntegerField(db_index=True, verbose_name=u'章序号')

    class Meta:
        verbose_name = u'章'
        verbose_name_plural = verbose_name
        ordering = ['number', ]

    def __str__(self):
        return self.name


class Section(TimeModel):
    DIFFICULTY_CHOICES = (
        (0, '简单'),
        (1, '中等'),
        (2, '困难'),
    )
    name = models.CharField(max_length=100, db_index=True, verbose_name=u'节名称')
    chapter = models.ForeignKey(Chapter, db_index=True, related_name='sections', verbose_name=u'所属章', on_delete=models.CASCADE)
    number = models.IntegerField(db_index=True, verbose_name=u'节序号')
    difficulty = models.PositiveIntegerField(choices=DIFFICULTY_CHOICES, verbose_name=u'难度')
    is_keypoint = models.BooleanField(verbose_name=u'是否重点')
    questions = models.ManyToManyField(Question, through='SectionQuestion', verbose_name=u'章节题目')

    class Meta:
        verbose_name = u'节'
        verbose_name_plural = verbose_name
        ordering = ['number', ]

    def __str__(self):
        return self.name


class SectionQuestion(TimeModel):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(verbose_name='序号')

    class Meta:
        ordering = ['number']
        unique_together = ['section', 'question']


class DayAttendance(models.Model):
    create_time = models.DateField(auto_now_add=True, unique=True, verbose_name=u'创建时间')
    analysis_file = models.CharField(max_length=100, verbose_name=u'笔记文件')
    questions = models.ManyToManyField(Question, through='DayQuestion', verbose_name='每日题目')

    class Meta:
        verbose_name = u'每日打卡'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '每日打卡:' + str(self.create_time)


class DayQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    day_attendance = models.ForeignKey(DayAttendance, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(verbose_name=u'序号')

    class Meta:
        ordering = ['number']
        unique_together = ['question', 'day_attendance']


class Examination(TimeModel):
    TYPE_CHOICE = (
        (0, '历年真题'),
        (1, '模拟题'),
    )
    name = models.CharField(max_length=100, db_index=True, verbose_name=u'试卷名称')
    questions = models.ManyToManyField(Question, through='ExamQuestion', verbose_name='试卷题目')
    number = models.IntegerField(verbose_name=u'试卷编号')
    exam_type = models.IntegerField(db_index=True, choices=TYPE_CHOICE, verbose_name=u'试卷类型')
    exam_time = models.PositiveIntegerField(default=120, verbose_name=u'考试时间')

    class Meta:
        verbose_name = u'试卷'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ExamQuestion(TimeModel):
    examination = models.ForeignKey(Examination, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    number = models.PositiveIntegerField(verbose_name='序号')

    class Meta:
        ordering = ['number']
        unique_together = ['examination', 'question']