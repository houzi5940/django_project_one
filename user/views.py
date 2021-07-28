from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import User

import hashlib
# Create your views here.

#注册
def reg_view(request):
    # pass
    if request.method =='GET':
        return render(request,'user/register.html')
    elif request.method =='POST':
        username = request.POST['username']
        password_1 = request.POST['password_1']
        password_2 = request.POST['password_2']

        #查看密码一致性
        if password_1!= password_2:
            HttpResponse('两次密码不一致')

        #哈希算法 - 给密码加密
        #特点 1、定长加密 - md5算法，32位16进制
        m = hashlib.md5()
        m.update(password_1.encode())
        password_m = m.hexdigest()

        #查看当前用户名是否可用
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('用户名已注册')
        
        #插入数据
        try:
            user = User.objects.create(username = username, password = password_m)
        except Exception as e:
            print('--create user error %s'%(e))
            return HttpResponse('用户名已注册')

        #免登录一天
        request.session['username'] = username
        request.session['uid'] = user.id

        return HttpResponseRedirect('/index/')

#登录
def login_view(request):
    if request.method == 'GET':
        #检擦登录页面
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index/')

        #检查cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_username and c_uid:
            #回写session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index/')

        return render(request,'user/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print('--login user error %s'%(e))
            return HttpResponse('用户名或密码错误')
        
        #比对密码
        m = hashlib.md5()
        m.update(password.encode())

        if m.hexdigest() != user.password:
            return HttpResponse('用户名或密码错误')

        #记入会话
        request.session['username'] =username
        request.session['uid'] = user.id 
        resp = HttpResponseRedirect('/index/')
        Three_days = 3600*24*3
        if 'remeber' in request.POST:
            resp.set_cookie('username',username, Three_days)
            resp.set_cookie('uid',user.id, Three_days)

        return resp

#退出登录
def logout_view(request):
    if 'username' in request.session :
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    resp = HttpResponseRedirect('/index/')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp

