from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(registration_form)
admin.site.register(Courses)

class AdminAttendance_db(admin.ModelAdmin):
	readonly_fields = ('time', )
admin.site.register(Attendance_db, AdminAttendance_db)

admin.site.register(Class_history)