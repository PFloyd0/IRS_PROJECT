from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate,login


def start(request):
    return render(request, 'login.html')


def my_login(request):
    message=''
    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            return render(request, 'index.html')
        else:
            message = '用户名或密码错误'
    return render(request, 'login.html', {'message': message})