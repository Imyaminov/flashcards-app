from django import forms
from .models import CustomUser

class CustomUserRegisterForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')
