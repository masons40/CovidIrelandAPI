from django.urls import path
from rest_framework import routers

from . import views


app_name = 'data_display'
urlpatterns = [
    path('', views.index, name='index'),
    path('upload', views.data_upload, name='data_upload'),
    path('delete', views.delete_data, name='delete_data'),
    path('addall', views.upload_all, name='upload_all')
]