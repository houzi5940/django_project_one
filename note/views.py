from user.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Note

# Create your views here.

#校验登录状态的装饰器
def check_login(fn):
    def wrap (request,*args,**kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_username or not c_uid:
                return HttpResponseRedirect('/user/login')
            else:
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return fn(request,*args,**kwargs)
    return wrap

@check_login 
def add_note(request):
    if request.method == 'GET':
        return render(request,'note/add_note.html')
    elif request.method =='POST':
        uid = request.session['uid']
        title = request.POST['title'] 
        content = request.POST['content']
        Note.objects.create(title = title,content = content,user_id = uid)
        return HttpResponseRedirect('/note/list')



@check_login
def list_note(request): 
    if request.method == 'GET':
        date = Note.objects.filter(user_id = request.session['uid'])
        return render(request,'note/list_note.html',locals())
