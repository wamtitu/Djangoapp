from django.db import models

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class CreateUserFrom(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class File(models.Model):
    
    date_created = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(null=True)
    file_name = models.CharField(max_length=200, null=True)
    fileType = models.CharField(max_length=200, null=True)
    deleted = models.BooleanField(null=True, default=False)