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


class SendResetPasswordEmailForm(Form):
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email'}),
                            required=True, )


class ResetPasswordForm(Form):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control', 'id': 'password', 'placeholder': 'Password'}),
                               required=True, )
    confirm_password = forms.CharField(label='Confirm password',
                                       widget=forms.PasswordInput(
                                           attrs={'class': 'form-control', 'id': 'confirm_password',
                                                  'placeholder': 'Confirm password'}),
                                       required=True, )
