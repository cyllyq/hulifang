import datetime

import ujson as json

from users.models import User, VerifyCode
from operation.models import QuestionFeedback
from apps.utils.tools import get_questions
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate
from apps.utils import tools
from apps.decorators import login_required


def send_code(request):
    '''
    发送验证码
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    code = tools.get_code()
    mobile = reqeust.POST.get('mobile')
    if send_code(mobile, code):
        VerifyCode.objects.create(mobile=mobile, code=code, expire_time=datetime.datetime.now()+datetime.timedelta(seconds=5*60))
    else:
        rsp_data['code'] = 205
        rsp_data['msg'] = '发送验证码失败'
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


def register(request):
    '''
    注册
    '''
    if request.method == 'POST':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        mobile = request.POST.get('mobile')
        vcode = VerifyCode.objects.filter(mobile=mobile, expire_time__gte=datetime.datetime.now())
        if vcode:
            code = request.POST.get('code')
            if vcode[0].code == code:
                if User.objects.filter(mobile=mobile).existe():
                    rsp_data['code'] = 205
                    rsp_data['msg'] = '用户已存在'
                else:
                    password = request.POST.get('passord')
                    user = User.objects.create_user(mobile=mobile, password=password)
                    vcode[0].is_used = True
                    vcode[0].save()
                    login(request, user)
            else:
                rsp_data['code'] = 206
                rsp_data['msg'] = '验证码错误'
        else:
            rsp_data['code'] = 207
            rsp_data['msg'] = '无效验证码'
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json,` charset=utf-8')


def login(request):
    '''
    登录
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    mobile = request.POST.get('mobile')
    password = request.POST.get('post')
    user = authenticate(mobile=mobile, password=password)
    if user is not None:
        login(request, user)
    else:
        rsp_data['code'] = 204
        rsp_data['msg'] = '用户名或密码错误'
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='applicaton/json, chartset=utf-8')


def logout(request):
    '''
    退出登录
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }


@login_required
def wrong_questions(request):
    '''
    用户错题集
    '''
    rsp_data = {
        'code': 200,
        'msg': '成功',    
    }
    data = {
        'questions': [],
    }

    kwargs = {
        'related': request.user,
        'question_type': 'wrong'
    }
    if request.user.is_authenticated:
        kwargs['user'] = request.user

    questions = get_questions(**kwargs)
    data['questions'] = questions
    rsp_data['data'] = data
    return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), 
        content_type="application/json, charset=utf-8")


@login_required
def question_feedback(request):
    '''
    用户反馈
    '''
    if request.method == 'POST':
        rsp_data = {
            'code': 200,
            'msg': '成功',    
        }
        user = request.user
        comment = request.POST.get('comment')
        question_id = request.POST.get('question_id')
        QuestionFeedback.objects.create(user=user, commment=comment, question__id=question_id)
        return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json, charset=utf-8')


def user_message(request, user_id):
    '''
    用户消息推送
    '''
    pass

