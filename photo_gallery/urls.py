from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_photo, name='upload_photo'),
]
