from django.shortcuts import render
from django.contrib.auth import authenticate,login
from . import models
from recommendation_system import hybird

def start(request):
    return render(request, 'login.html')


def my_login(request):
    message=''
    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            User_cast = models.User_cast.objects.get(user=user)
            book_re = hybird.do_recommendation(User_cast.cast_id)
            re = []
            for row in book_re.itertuples():
                re.append({'name': getattr(row, 'Name_x'), 'id': getattr(row, 'Id_x')})
            print(re)
            return render(request, 'index.html', {'book_list': re})
        else:
            message = '用户名或密码错误'
    return render(request, 'login.html', {'message': message})