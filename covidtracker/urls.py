from django.urls import path
from rest_framework import routers

from . import views


app_name = 'data_display'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.data_upload, name='data_upload'),
    path('delete', views.delete_data, name='delete_data'),
    path('addall', views.upload_all, name='upload_all'),
    path('home', views.home, name="home"),
    path('logout', views.logout_view, name="logout_view"),
    path('slform', views.slform, name="slform"),
    path('about', views.about, name="about"),
    path('endpoints', views.endpoints, name="endpoints"),
    path('loginuser', views.loginuser, name="loginuser")
]