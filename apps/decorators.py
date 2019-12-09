'''
@Author: your name
@Date: 2019-12-10 22:47:20
@LastEditTime: 2019-12-10 23:07:46
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: \hulifang\apps\decorators.py
'''
import ujson as json
from functools import wraps

from django.http import HttpResponse


def login_required(func):
    @wraps(func)
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        else:
            rsp_data = {
                'code': 201,
                'msg': '未登录',
            }
            return HttpResponse(json.dumps(rsp_data, ensure_ascii=False), content_type='application/json charset=utf-8')
    return wrapped_view
