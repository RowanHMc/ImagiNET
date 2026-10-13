from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('upload/', views.upload_photo, name='upload_photo'),
    path('photos/<int:photo_id>/', views.photo_detail, name='photo_detail'),
    path('photos/<int:photo_id>/react/', views.react_to_photo, name='react_to_photo'),

]
