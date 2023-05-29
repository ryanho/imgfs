from django.shortcuts import render
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from .forms import CustomAuthenticationForm
from django.conf import settings

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'customauth/login.html'
    authentication_form = CustomAuthenticationForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hcaptcha_sitekey'] = settings.HCAPTCHA_SITEKEY
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            data = kwargs['data'].copy()
            data['hcaptcha'] = self.request.POST.get('h-captcha-response', None)
            kwargs.update({
                'data': data
            })
        return kwargs


class CustomLogoutView(LogoutView):
    pass


class CustomPasswordResetView(PasswordResetView):
    pass
