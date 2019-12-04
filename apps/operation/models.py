from django.db import models
from apps.abstract import TimeModel
from django.conf import settings
from examination.models import Question, Examination, DayAttendance, Section, SectionQuestion


User = settings.AUTH_USER_MODEL


class QuestionFeedback(TimeModel):
    user = models.ForeignKey(User, verbose_name=u'反馈用户', on_delete=models.DO_NOTHING)
    question = models.ForeignKey(Question, verbose_name=u'反馈问题', on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, db_index=True, verbose_name=u'反馈内容')
    has_handle = models.BooleanField(default=False, verbose_name=u'是否处理')

    class Meta:
        verbose_name = u'问题反馈'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment


class QuestionFav(TimeModel):
    user = models.ForeignKey(User, verbose_name=u'用户', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=u'收藏问题', on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'问题收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class WrongQuestion(TimeModel):
    user = models.ForeignKey(User, verbose_name=u'用户', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name=u'错题', on_delete=models.CASCADE)
    wrong_count = models.PositiveIntegerField(default=1, verbose_name='错误次数')

    class Meta:
        verbose_name = u'错题集'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user


class UserMessage(TimeModel):
    user = models.ForeignKey(User, verbose_name=u'用户', on_delete=models.CASCADE)
    message = models.CharField(max_length=300, verbose_name=u'信息')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')

    class Meta:
        verbose_name = u'系统消息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class ExamScore(TimeModel):
    user = models.ForeignKey(User, verbose_name=u'用户', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(verbose_name=u'成绩')
    examination = models.ForeignKey(Examination, verbose_name=u'所属试卷', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '试卷成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.score


class DayScore(TimeModel):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    score = models.PositiveIntegerField(verbose_name=u'成绩')
    day_attendance = models.ForeignKey(DayAttendance, verbose_name=u'所属日期', on_delete=models.CASCADE)
    is_done = models.BooleanField(default=False, verbose_name='是否做完')
    question = models.ForeignKey(Question, null=True, blank=True, verbose_name='做到哪一题', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '每日打卡成绩'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.score


class SectionRecord(TimeModel):
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    section_question = models.ForeignKey(SectionQuestion, verbose_name='做到哪一题', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, verbose_name='所属节', on_delete=models.CASCADE)
    #is_done = models.BooleanField(default=False, verbose_name='是否做完')

    class Meta:
        verbose_name = '章节记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.question