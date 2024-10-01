# myapp/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')

class LoginForm(AuthenticationForm):
    pass

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)