from django.db import models


class TimeModel(models.Model):
    """
    包含创建和修改时间的基础类
    """

    create_time = models.DateTimeField(auto_now_add=True, verbose_name=u'创建时间')
    modify_time = models.DateTimeField(auto_now=True, verbose_name=u'更新时间')

    class Meta:
        abstract = True



class DelModel(models.Model):
    """
    记录是否删除的基础类
    """
    is_delete = models.BooleanField(default=False, verbose_name=u'是否删除')

    class Meta:
        abstract = True


class QuestionModel(models.Model):
    """
    问题的基础类
    """
    TYPE_CHOICE = (
        (0, '单选题'),
        (1, '多选题'),
        (2, '判断题'),
    )

    question_type = models.PositiveIntegerField(default=0, choices=TYPE_CHOICE)
    title = models.CharField(max_length=200, verbose_name=u'题目')
    stem = models.CharField(max_length=200, null=True, blank=True, verbose_name=u'题干')
    number = models.IntegerField(verbose_name=u'序号')
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
        abstract = True
        ordering = ['number', ]

    def __str__(self):
        return self.title