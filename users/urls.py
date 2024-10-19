from django.urls import path
from .views import SignUpView, CustomLogoutView


app_name = 'users'
urlpatterns = [

    path('signup/', SignUpView.as_view(), name='signup'),
    path('users/logout/', CustomLogoutView.as_view(), name='logout'),
]
