from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from . import models
from recommendation_system import rbm_cf_books_tf2

def start(request):
    return render(request, 'login.html')


def my_login(request):
    message=''
    if request.method == "POST":
        user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
        if user:
            login(request, user)
            User_cast = models.User_cast.objects.get(user=user)
            book_re = rbm_cf_books_tf2.do_recommendation(User_cast.cast_id)
            book_name = book_re['Name_x']
            print(book_name)
            re = {}
            for i in range(len(book_name)):
                re["name%d"%i] = book_name.iloc[i]
            print(re)
            return render(request, 'index.html', re)
        else:
            message = '用户名或密码错误'
    return render(request, 'login.html', {'message': message})