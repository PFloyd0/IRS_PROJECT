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