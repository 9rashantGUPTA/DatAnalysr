from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import *


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = '__all__'
        exclude = ['updated']


class BrandForm(ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'
        exclude = ['slug', 'created']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



