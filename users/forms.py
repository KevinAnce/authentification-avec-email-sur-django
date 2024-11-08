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


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='Current Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'current_password', 'placeholder': 'Current Password'}
        ),
        required=True,
    )
    new_password = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'new_password', 'placeholder': 'New Password'}
        ),
        required=True,
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'id': 'confirm_password', 'placeholder': 'Confirm Password'}
        ),
        required=True,
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.user.check_password(current_password):
            raise forms.ValidationError("The current password is incorrect.")
        return current_password

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "The new passwords do not match.")

        return cleaned_data
