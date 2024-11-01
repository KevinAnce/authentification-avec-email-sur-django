from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

from users.models import User


class PasswordResetTokenGeneration(PasswordResetTokenGenerator):
    def _make_hash_value(self, user: User, timestamp: int) -> str:
        return (
                six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.password)
        )


password_reset_token = PasswordResetTokenGeneration()
