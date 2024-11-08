from django.urls import path

from .views import SignUpView, CustomLogoutView, VerifyEmailView, resend_verification_email, reset_password, \
    SendResetPasswordEmailView, ChangePasswordView

app_name = 'users'
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/<int:user_id>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-email/<int:user_id>/', resend_verification_email, name='resend-verification-email'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),
    path('send-reset-password-link/', SendResetPasswordEmailView.as_view(), name='send-reset-password-link'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]
