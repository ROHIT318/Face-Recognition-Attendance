from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from .getdetails import getDetails
from .register import storeImage, startTraining

def home(request):
    return render(request, 'Index.html')

def startCamera(request):
    name = getDetails()
    return redirect('displayName', name)

def displayName(request, name):
    context = {'name': name}
    return render(request, 'name_check.html', context)


# For test purpose only
def register(request):
    if request.method == 'POST':
        msg = storeImage(request.POST['unique_id'], request.POST['student_name'])
        context = {'msg': msg}
        return render(request, 'del_msg.html', context)
    return render(request, 'del_register.html')

def imageShow(request):
    imgs = registration_form.objects.all()
    context = {'Imgs': imgs}
    return render(request, 'show_image.html', context)

def train(request):
    message = startTraining()
    context = {'msg': message}
    return render(request, 'del_msg.html', context)

def showId(request):
    unique_id_list = list()
    students = registration_form.objects.all()
    for student in students:
        unique_id_list.append(student.unique_id)
    context = {'msg': unique_id_list}
    return render(request, 'del_msg.html', context)