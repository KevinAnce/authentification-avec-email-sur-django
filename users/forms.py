from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email',)


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('email', 'password')
