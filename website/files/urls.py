from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.index, name="index"),
    path('', views.loginpage, name="login"),
    path('register/', views.registerpage, name="register"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('list_files/', views.list_files, name="list_files"),
    path('download_file/<int:file_id>/', views.download_file, name="download_file"),
    path('delete_file/<int:file_id>/', views.delete_file, name="delete_file"),
]