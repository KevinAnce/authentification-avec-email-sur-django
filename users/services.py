import datetime
import random

from django.conf import settings
from django.utils import timezone

from users.exceptions import OtpVerifyError
from users.models import User, Otp


class OtpService:
    def __init__(self):
        self.number_of_digits = settings.OTP_CODE_NUMBER_OF_DIGITS

    def create(self, user: User) -> Otp:
        digits = self.__get_digits()
        otp = Otp.objects.create(
            code=str(random.randrange(0, digits)).zfill(self.number_of_digits),
            expiration_at=timezone.now()
                          + datetime.timedelta(minutes=settings.OTP_VALID_MINUTES),
            user_id=user.id,
        )
        return otp

    def __get_digits(self) -> int:
        digits = ""
        for num in range(self.number_of_digits):
            digits += "9"
        return int(digits)


class OtpVerifyService:
    def done(self, user: User, send_code: str):
        if not user.otp_set.all():
            raise OtpVerifyError("Invalid otp verify")
        otp = user.otp_set.all().last()
        if send_code != otp.code:
            raise OtpVerifyError("Wrong otp code")
        if timezone.now() > otp.expiration_at:
            raise OtpVerifyError("Expiration of validity")
        self.verify_done(user)

    def verify_done(self, user: User) -> None:
        user.email_verified_at = timezone.now()
        user.last_login = timezone.now()
        user.save()
