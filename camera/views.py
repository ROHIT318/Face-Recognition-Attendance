from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .getdetails import getdetails

def home(request):
    return render(request, 'Index.html')

def startCamera(request):
    name = getdetails()
    return redirect('displayName', name)

def displayName(request, name):
    context = {'name': name}
    return render(request, 'name_check.html', context)