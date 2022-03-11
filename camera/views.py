from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .getdetails import getdetails
from .register import showImage

def home(request):
    return render(request, 'Index.html')

def startCamera(request):
    name = getdetails()
    return redirect('displayName', name)

def displayName(request, name):
    context = {'name': name}
    return render(request, 'name_check.html', context)


# For test purpose only
def register(request):
    if request.method == 'POST':
        msg = showImage(request.POST['unique_id'], request.POST['student_name'])
        context = {'msg': msg}
        return render(request, 'del_msg.html', context)
    return render(request, 'del_register.html')

def imageShow(request):
    imgs = registration_form.objects.all()
    context = {'Imgs': imgs}
    return render(request, 'show_image.html', context)