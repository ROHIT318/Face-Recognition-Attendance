from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

# app_name = camera

urlpatterns = [
    path('', views.home, name='home'),
    path('displayName/<str:name>', views.displayName, name='displayName'),
    path('startCamera/', views.startCamera, name='startCamera'),
    path('register/', views.register, name='register'),

    # For test purpose
    path('imageShow/', views.imageShow, name='imageShow'),
    path('train/', views.train, name='train'),
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)