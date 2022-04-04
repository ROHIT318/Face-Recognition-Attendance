from django.db import models
from django.contrib.auth.models import User
import datetime

# Registration table (Img test pending)
class registration_form(models.Model):
	unique_id = models.CharField(max_length=10, primary_key=True)
	name = models.CharField(max_length=60)
	email = models.EmailField(default='a@a.com')
	is_active = models.BooleanField(default=True)
	img_1 = models.ImageField(upload_to='pics')
	img_2 = models.ImageField(upload_to='pics')
	img_3 = models.ImageField(upload_to='pics')
	img_4 = models.ImageField(upload_to='pics')
	img_5 = models.ImageField(upload_to='pics')
	img_6 = models.ImageField(upload_to='pics')
	img_7 = models.ImageField(upload_to='pics')

	def __str__(self):
		return self.unique_id + ": " + self.name


# Courses offered by institution (DONE)
class Courses(models.Model): 
	subject_code = models.CharField(max_length=10, primary_key=True)
	teacher_name = models.CharField(max_length=20, blank=False)

	def __str__(self):
		return self.subject_code


# Attendance sheet
class Attendance_db(models.Model):
	subject_code = models.CharField(max_length=10)
	unique_id = models.CharField(max_length=10)
	date = models.DateField(default=datetime.date.today, blank=False)
	time = models.TimeField(auto_now_add=True, blank=False)

	def __str__(self):
		return self.subject_code + ": " + self.unique_id


# All classes conducted in institution
class Class_history(models.Model):
	subject_code = models.CharField(max_length=10)
	teacher_name = models.CharField(max_length=30, blank=False)
	date_conducted = models.DateField(default=datetime.date.today, blank=False)
	time_started = models.TimeField(auto_now_add=True, blank=False)

	def __str__(self):
		return self.subject_code + ": " + self.date_conducted

