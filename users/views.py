import smtplib

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic.edit import CreateView

from .emails import send_opt, send_reset_password_link
from .exceptions import OtpVerifyError
from .forms import CustomUserCreationForm, VerificationEmailForm, SendResetPasswordEmailForm, ResetPasswordForm, \
    ChangePasswordForm
from .models import User
from .services import OtpVerifyService, OtpService
from .tokens import password_reset_token


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


class SendResetPasswordEmailView(View):
    def get(self, request):
        form = SendResetPasswordEmailForm()
        return render(self.request, template_name='registration/send_reset_password_email.html', context={"form": form})

    def post(self, request):
        form = SendResetPasswordEmailForm(self.request.POST)
        if form.is_valid():
            try:
                user = User.objects.get(email=form.cleaned_data['email'])
                with transaction.atomic():
                    try:
                        send_reset_password_link(request, user)
                        messages.success(request, "We have sent reset password mail", "success")
                    except smtplib.SMTPException:
                        messages.error(request, "Error when sending mail please try again later", "danger")
            except User.DoesNotExist:
                messages.error(request, "User with this email address does not exist", "danger")
        return render(request, template_name='registration/send_reset_password_email.html', context={"form": form})


def reset_password(request, uidb64, token):
    form = ResetPasswordForm()
    context = {}
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetPasswordForm(request.POST)
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                messages.success(request, "Your password has been reset.", "success")
                return redirect("login")
    else:
        context['error'] = True
    context['form'] = form
    return render(request, template_name='registration/reset_password.html', context=context)


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = ChangePasswordForm(user=request.user)
        return render(self.request, template_name='registration/change_password.html', context={"form": form})

    def post(self, request):
        form = ChangePasswordForm(user=self.request.user, data=request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            try:
                with transaction.atomic():
                    request.user.set_password(new_password)
                    request.user.save()
                    messages.success(request, "Your password has been changed successfully.",
                                     extra_tags="success")
                    return redirect("login")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}", extra_tags="danger")
        else:
            # Handle form errors (e.g., current password incorrect, passwords do not match)
            messages.error(request, "Please correct the errors below.", extra_tags="warning")

        return render(request, 'registration/change_password.html', context={"form": form})
