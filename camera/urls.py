from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('train/', views.train, name='train'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('showAttendance/', views.showAttendance, name='showAttendance'),
    path('registerStudent/', views.registerStudent, name='registerStudent'),
    path('registerTeacher/', views.registerTeacher, name='registerTeacher'),
    path('startAttendance/', views.startAttendance, name='startAttendance'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)