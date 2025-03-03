from django import forms
from .models import Page
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'image']

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
