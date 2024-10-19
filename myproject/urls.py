from django.contrib import admin
from django.urls import path, include

from users.views import profile_view, home_view

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/profile/', profile_view, name='profile'),
]
