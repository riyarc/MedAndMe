from django import forms
# from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=[x for x in range(1940, 2021)]))

    class Meta:
        model = User
        fields = ['username', 'date_of_birth', 'email', 'password1', 'password2']
