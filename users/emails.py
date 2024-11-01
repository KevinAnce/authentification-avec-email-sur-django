from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.tokens import password_reset_token


def send_mail(subject, body, to):
    email = EmailMessage(
        subject=subject, body=body, from_email=settings.EMAIL_FROM, to=to
    )
    email.content_subtype = 'html'
    email.send()


def send_opt(otp):
    subject = "OTP Verification"

    body = f"Your is {otp.code}\n It's valid {settings.OTP_VALID_MINUTES}"

    to_email = otp.user.email

    send_mail(subject, body, [to_email])


def send_reset_password_link(request, user):
    subject = 'Reset your password'
    domain = get_current_site(request).domain
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    link = f'http://{domain}{reverse("users:reset-password", kwargs={"uidb64": uid, "token": token})}' # noqa
    body = f'Click <a href={link}>here</a> to reset your password.'
    send_mail(subject, body, [user.email])
