from django.shortcuts import render
from django.contrib.auth.models import User


# 接收POST请求数据
def register(request):
    info = {}
    try:
        User.objects.get(username=request.POST['username'])
        info['lala'] = '用户名已存在'
    except:
        if request.POST['password'] == request.POST['password_2'] and len(request.POST['password']) != 0:
            User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
            info['lala'] = request.POST['username']
            return render(request, 'login.html', info)
        else:
            info['lala'] = '两次密码不同或未输入密码'
    return render(request, "register.html", info)

