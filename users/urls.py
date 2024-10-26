from django.urls import path
from .views import SignUpView, CustomLogoutView, VerifyEmailView, resend_verification_email

app_name = 'users'
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/logout/', CustomLogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('verify-email/<int:user_id>/', VerifyEmailView.as_view(), name='verify-email'),
    path('resend-verification-email/<int:user_id>/', resend_verification_email, name='resend-verification-email'),
]
