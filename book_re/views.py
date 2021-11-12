from django.shortcuts import render

from recommendation_system import hybird
from .import models
import tkinter.messagebox
from django.db.models import Count
from django.contrib import messages
from tkinter import *
from django.http import HttpResponseRedirect
from django.urls import reverse
from SentimentParser import main
# Create your views here.


def go(request,nid):
    message = {}
    page = nid +'.html'
    user = request.user
    User_cast = models.User_cast.objects.get(user=user)
    book_re = hybird.do_recommendation(User_cast.cast_id)
    re = []
    for row in book_re.itertuples():
        re.append({'name': getattr(row, 'Name_x'), 'id': getattr(row, 'Id_x')})
    print(re)
    a = models.Chat_record.objects.filter(user=User_cast.cast_id)
    a.delete()
    return render(request, page, {'book_list': re})


def detail(request, nid):
    book = models.Books.objects.get(id=nid)
    return render(request, "detail.html", {"book":book})


def rating(request, nid):
    cast_id = models.User_cast.objects.get(user=request.user).cast_id
    try:
        book_rating = models.Bookrating.objects.get(user_id=cast_id, name=nid)
        book_rating.rating = request.POST['rating']
        book_rating.save()
    except:
        book_rating = models.Bookrating.objects.create(user_id=cast_id, name=nid, rating=request.POST['rating'])
        book_rating.save()
    book = models.Books.objects.get(id=nid)
    return render(request, "detail.html", {"book": book})


def search(request):
    book = models.Books.objects.filter(name__contains=request.POST['book_name'])
    return render(request, "index.html", {"book_list": book})


def my(request):
    user = request.user
    User_cast = models.User_cast.objects.get(user=user)
    li = models.Bookrating.objects.filter(user_id=User_cast.cast_id)[:20]
    re = []
    for i in li:
        re.append({"rating": i.rating, "name": models.Books.objects.get(id=i.name).name, "id": i.name})
    return render(request, "my.html", {"book_list": re})


def wishlist(request):
    user = request.user
    User_cast = models.User_cast.objects.get(user=user)
    li = models.Bookrating.objects.filter(user_id=User_cast.cast_id)[:20]
    re = []
    for i in li:
        re.append({"rating": i.rating, "name": models.Books.objects.get(id=i.name).name, "id": i.name})
    return render(request, "wishlist.html", {"book_list": re})


def chat(request):
    question = request.POST['question']
    user = request.user
    User_cast = models.User_cast.objects.get(user=user).cast_id
    answer = main.do_chat(question, User_cast)
    record = models.Chat_record.objects.create(question=question, answer=answer, user=User_cast)
    record.save()
    messages = models.Chat_record.objects.filter(user=User_cast)
    return render(request, "chat.html", {"message": messages})