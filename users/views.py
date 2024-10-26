import smtplib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic.edit import CreateView

from .emails import send_opt
from .exceptions import OtpVerifyError
from .forms import CustomUserCreationForm, VerificationEmailForm
from .models import User
from .services import OtpVerifyService, OtpService


def home_view(request):
    return render(request, 'home.html')


@login_required(login_url='login')
def profile_view(request):
    return render(request, 'registration/profile.html')


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse('users:verify-email', kwargs={'user_id': self.object.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.instance
        with transaction.atomic():
            otp = OtpService().create(user)
            messages.success(self.request, "We have send a verification mail", "success")
            try:
                send_opt(otp)
            except smtplib.SMTPException:
                user.delete()
                messages.error(self.request, "Error when sending mail please try again later", "danger")
        return response


class VerifyEmailView(View):
    template_name = 'registration/verification.html'

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = VerificationEmailForm()
        return render(self.request, template_name=self.template_name, context={"form": form, "user_id": user.id})

    def post(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        form = VerificationEmailForm(self.request.POST)
        if form.is_valid():
            try:
                otp = form.cleaned_data["otp"]
                OtpVerifyService().done(user, otp)
                messages.success(request, "Verification successful", "success")
                return redirect("login")
            except OtpVerifyError as e:
                messages.success(request, e, "success")
        return render(self.request, template_name=self.template_name, context={"form": form, "user_id": user.id})


def resend_verification_email(request, user_id):
    user = get_object_or_404(User, id=user_id)
    with transaction.atomic():
        otp = OtpService().create(user)
        messages.success(request, "We have resend a verification mail", "success")
        try:
            send_opt(otp)
        except smtplib.SMTPException:
            user.delete()
            messages.error(request, "Error when sending mail please try again later", "danger")
        return redirect(reverse("users:verify-email", kwargs={"user_id": user.id}))


class CustomLogoutView(LogoutView):
    template_name = 'registration/logout.html'

    def get_next_page(self):  # noqa
        return '/'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
