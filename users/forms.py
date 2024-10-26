from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import Form

from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')


class VerificationEmailForm(Form):
    otp = forms.CharField(max_length=7, min_length=7, label='OTP',
                          widget=forms.NumberInput(
                              attrs={'class': 'form-control', 'id': 'otp', 'placeholder': 'OTP Code'}),
                          required=True, )
