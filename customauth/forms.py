from django import forms
from django.contrib.auth.forms import AuthenticationForm
from backend.forms import HCaptchaField


class CustomAuthenticationForm(AuthenticationForm):
    hcaptcha = HCaptchaField()
