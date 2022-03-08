from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('displayName/<str:name>', views.displayName, name='displayName'),
    path('startCamera/', views.startCamera, name='startCamera'),
]