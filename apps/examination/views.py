import datetime

import ujson as json

from .models import Chapter, Section, Question, Examination, SectionQuestion, \
    ExamQuestion, DayQuestion, DayAttendance
from operation.models import SectionRecord, ExamScore, DayScore, QuestionFav, WrongQuestion
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db.models import Count, F, Value, IntegerField
from apps.utils.tools import get_questions, correct_question_count
from apps.decorators import login_required


def section_list(request):
    '''
    返回章节列表
    return {
        
    }
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    chapter_records = Chapter.objects.all().prefetch_related('sections',)
    data = {'chapters':[]}

    section_ids = []
    section_records = {}

    #获取用户的章节习题记录
    if request.user.is_authenticated:
        user = request.user
        section_records = dict(SectionRecord.objects.values_list('section__id', 'section_question__number',).filter(user=user))
        section_ids = section_records.keys()

    for chapter_record in chapter_records:
        chapter = {}
        chapter['name'] = chapter_record.name
        chapter['id'] = chapter_record.id
        sections = []
        for section_record in chapter_record.sections.all().annotate(question_count=Count('questions')):
            section = {}
            section['id'] = section_record.id
            section['number'] = section_record.number
            section['name'] = section_record.name
            section['difficulty'] = section_record.difficulty
            section['is_keypoint'] = section_record.is_keypoint
            section['question_count'] = section_record.question_count
            section['current_num'] = section_records[section['id']] if section['id'] in section_ids else 0
            sections.append(section)
        chapter['sections'] = sections
        data['chapters'].append(chapter)
    rsp_data['data'] = data


    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
        content_type="application/json, charset=utf-8")
    #return JsonResponse(rsp_data)


def section_questions(request, section_id):
    '''
    返回章节所属题目
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    data = {
        'section_id': section_id,
        'questions': [],
    }

    kwargs = {
        'related': section_id,
        'question_type': 'section'
    }
    if request.user.is_authenticated:
        kwargs['user'] = request.user

    questions = get_questions(**kwargs)
    data['questions'] = questions
    rsp_data['data'] = data
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
        content_type="application/json, charset=utf-8")


def exam_list(request):
    '''
    返回试卷列表
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    data = {
        'exam': [],
    }
    #默认取试卷分数为-1，即为没做过的试卷
    exam_records = Examination.objects.all().annotate(score=Value(-1, IntegerField())).values('id', 'number', 'name', 'exam_type', 'exam_time', 'score')
    
    #标注已完成试卷分数
    if request.user.is_authenticated:
        score_records = dict(ExamScore.objects.filter(user=user,).values_list('examination__id', 'score'))
        exam_ids = score_records.keys()
        for exam_record in exam_records:
            exam_id = exam_record['id']
            if exam_id in exam_ids:
                exam_record['score'] = score_records[exam_id]


    data['exam'].extend(exam_records)
    rsp_data['data'] = data
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
        content_type="application/json, charset=utf-8")


@login_required
def examination(request, exam_id):
    '''
    获取试卷题目
    '''
    #get方法返回试卷题目
    
    if request.method == 'GET':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }   
        data = {
            'exam_id': exam_id,
            'questions': [],
        }

        kwargs = {
            'related': exam_id,
            'question_type': 'exam',
            'with_analysis': False,
            'with_answer': False,
        }
        #if request.user.is_authenticated:
        kwargs['user'] = user

        data['questions'] = get_questions(**kwargs)
        rsp_data['data'] = data
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
            content_type="application/json, charset=utf-8")

    #post方法计算试卷分数
    elif request.method == 'POST':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        questions = json.loads(request.body.decode('utf-8'))

        total, right_count = correct_question_count(questions, related=exam_id, question_type='exam')
        
        #暂时先将试卷的分数记为答对的题目数
        score = right_count

        ExamScore.objects.update_or_create(user=request.user, examination__id=exam_id, default={'score':score})

        rsp_data['data'] = {
            'total': total,
            'right_count': right_count,
            'score': score,
        }
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
            content_type="application/json, charset=utf-8")


@login_required
def dayattendance(request):
    '''
    获取每日打卡题目
    '''
    #get方法返回每日打卡题目
    if request.method == 'GET':
        day = datetime.date.today()
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        data = {
            'day': str(day),
            'questions': [],
        }

        kwargs = {
            'related': day,
            'question_type': 'day',
        }
        #if request.user.is_authenticated:
        kwargs['user'] = request.user

        data['questions'] = get_questions(**kwargs)
        rsp_data['data'] = data
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False),
            content_type="application/json, charset=utf-8")

    #post方法计算每日打卡分数
    elif request.method == 'POST':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        request_data = json.loads(request.body.decode('utf-8'))
        questions = request_data['questions']
        day = request_data['day']
        related = datetime.date.today()
        if day != str(related):
            rsp_data['code'] = 202
            rsp_data['msg'] = '已过打卡时间'
            return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')

        total, right_count = correct_question_count(questions, related=related, question_type='day')

        #每日打卡的分数即视为做对的题目数
        score = right_count

        try:
            dayattendance = DayAttendance.objects.get(create_time=related)
        except DayAttendance.DoesNotExist:
            rsp_data['code'] = 203
            rsp_data['msg'] = '打卡不存在'
            return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')

        DayScore.objects.update_or_create(user=request.user, day_attendance=dayattendance, defaults={'score': score})

        rsp_data['data'] = {
            'total': total,
            'right_count': right_count,
            'score': score,
        }
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
            content_type="application/json, charset=utf-8")


@login_required
def section_record(request, section_id):
    '''
    记录章节的答题位置
    '''
    if request.method == 'POST':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        question_id = request.POST.get('question_id')
        SectionRecord.objects.update_or_create(user=request.user, section__id=section_id, defaults={'section_question': question_id})
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


@login_required
def question_fav(request, question_id):
    '''
    用户问题收藏
    '''
    if request.method == 'POST':
        #if request.user.is_authenticated:
        rsp_data = {
            'code': 200,
            'msg': '',    
        }
        obj, created = QuestionFav.objects.get_or_create(user=request.user, question_id=question_id)
        if created:
            rsp_data['msg'] = '收藏成功'
        else:
            obj.delete()
            rsp_data['msg'] = '取消收藏'
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


@login_required
def add_wrong_question(request, question_id):
    '''
    添加错题记录，存在则增加错误次数
    '''
    #if request.user.is_authenticated:
    #存在则增加错误次数
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    WrongQuestion.objects.update_or_create(user=request.user, question_id=question_id, defaults={'wrong_count': F('wrong_count')+1})
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
        content_type="application/json, charset=utf-8")