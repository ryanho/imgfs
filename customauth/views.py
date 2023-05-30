from django.shortcuts import render
from .forms import CustomLoginForm, CustomSignupForm
from allauth.account.views import LoginView, SignupView

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'account/login.html'
    form_class = CustomLoginForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data'].copy()
            data['hcaptcha'] = self.request.POST.get('h-captcha-response', None)
            kwargs.update({
                'data': data
            })
        return kwargs


class CustomSignupView(SignupView):
    template_name = 'account/signup.html'
    form_class = CustomSignupForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data'].copy()
            data['hcaptcha'] = self.request.POST.get('h-captcha-response', None)
            kwargs.update({
                'data': data
            })
        return kwargs
