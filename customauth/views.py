from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'customauth/login.html'


class CustomLogoutView(LogoutView):
    pass


class CustomPasswordResetView(PasswordResetView):
    pass
