from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import TextInput,Textarea


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)
    
class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2']
        widgets = {
        "username": TextInput(attrs={"type": "text"}),
        "email": TextInput(attrs={"type": "text"}),
        "password1": TextInput(attrs={"type": "password"}),
        "password2": TextInput(attrs={"type": "password"})}