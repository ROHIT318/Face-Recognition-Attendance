from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User, auth
from .getdetails import getDetails
from .register import storeImage, startTraining


def home(request):
    return render(request, 'Index.html')

def aboutUs(request):
    return render(request, 'about_us.html')


# register both teacher and their courses
def registerTeacher(request):
    if request.method == "POST":
        t_id = request.POST['t_id']
        t_pswd = request.POST['t_pswd']
        t_first_name = request.POST['t_first_name']
        t_last_name = request.POST['t_last_name']
        t_subjectcode = request.POST['t_subjectcode']

        user = User.objects.create_user(username=t_id, password=t_pswd, 
            first_name=t_first_name, last_name=t_last_name, is_staff=True)
        user.save()
        tName = t_first_name + " " + t_last_name
        course = Courses.objects.create(subject_code=t_subjectcode, teacher_name=tName)
        course.save()
        return redirect('home')
    else:
        return render(request, 'register_teacher.html')


def startAttendance(request):
    if request.method == "POST":
        t_id = request.POST['t_id']
        t_pswd = request.POST['t_pswd']

        user = auth.authenticate(username=t_id, password=t_pswd)
        if user is not None:
            auth.login(request, user)
            request.session['subject_code'] = request.POST['subject_code']
            newClass = Class_history.objects.create(subject_code=request.session['subject_code'],
                teacher_name=request.POST['teacher_name'])
            newClass.save()
            return redirect('showAttendance')
        else:
            context = {'msg': "Invalid Login Credentials"}
            return render(request, 'take_attendance.html', context)
    else:
        return render(request, 'take_attendance.html')


# Responsible for showing and taking attendance
def showAttendance(request):
    if request.method=='POST':
        unique_id = getDetails()

        markStudentPresent = Attendance_db.objects.create(
            subject_code=request.session['subject_code'], unique_id=unique_id)
        markStudentPresent.save()

        allStudentsPresent = Attendance_db.objects.filter(date=datetime.date.today(), 
                subject_code=request.session['subject_code'])
        # Appending name column in attendance list
        for student in allStudentsPresent:
            studentInformation = registration_form.objects.filter(unique_id=student.unique_id)
            student.full_name = studentInformation[0].name

        context = {'allStudentsPresent': allStudentsPresent}
        return render(request, 'show_attendance.html', context)
    else:
        return render(request, 'show_attendance.html')


# For test purpose only
def registerStudent(request):
    if request.method == "POST":
        msg = storeImage(request.POST['s_unique_id'], request.POST['s_name'], 
            request.POST['s_email'])
        context = {'msg': msg}

        # return render(request, 'del_msg.html', context)
        # student = registration_form.objects.create(unique_id=request.POST['s_unique_id'], 
        #     email=request.POST['s_email'], name=request.POST['s_name'])
        # student.save()
        # context = {'msg': "Student saved successfully."}

        return render(request, 'register_student.html', context)
    else:
        return render(request, 'register_student.html')

def train(request):
    message = startTraining()
    context = {'msg': message}
    # context = {'msg': "Maintanance On."}
    return render(request, 'Index.html', context)
