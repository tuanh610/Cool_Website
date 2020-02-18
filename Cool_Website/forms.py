from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegisterForm(UserCreationForm):
    """
    A class used to represent the user register form
    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']