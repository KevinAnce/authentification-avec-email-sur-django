from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from .forms import CustomUserCreationForm


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'registration/profile.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def get_next_page(self):  # noqa
        return '/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
