from django.conf import settings
from django.core.mail import EmailMessage


def send_mail(subject, body, to):
    email = EmailMessage(
        subject=subject, body=body, from_email=settings.EMAIL_FROM, to=to
    )
    email.send()


def send_opt(otp):
    subject = "Vérification OTP"

    body = f"Your is {otp.code}\n It's valid {settings.OTP_VALID_MINUTES}"

    to_email = otp.user.email

    send_mail(subject, body, [to_email])
