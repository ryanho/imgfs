from django import forms
from django.contrib.auth.forms import AuthenticationForm
from backend.forms import HCaptchaField
from allauth.account.forms import LoginForm, SignupForm


class CustomLoginForm(LoginForm):
    hcaptcha = HCaptchaField()


class CustomSignupForm(SignupForm):
    hcaptcha = HCaptchaField()