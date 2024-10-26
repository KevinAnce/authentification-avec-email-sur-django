# myapp/middleware.py
from django.contrib import messages
from django.contrib.auth import authenticate
from django.shortcuts import redirect
from django.urls import reverse


class InactiveUserRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == reverse('login') and request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None and not user.email_verified_at:
                messages.warning(request, 'Account not verified, verify your email box or send another verification '
                                          'email.',
                                 extra_tags='warning')
                return redirect(reverse('users:verify-email', kwargs={"user_id": user.id}))

        return self.get_response(request)
