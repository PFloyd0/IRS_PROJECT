from django.shortcuts import render
from .import models
import tkinter.messagebox
from django.db.models import Count
from django.contrib import messages
from tkinter import *
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.


def go(request,nid):
    message = {}
    page = nid +'.html'
    message['hello'] = nid
    return render(request, page, message)


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
