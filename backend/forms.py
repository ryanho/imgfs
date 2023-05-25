from django import forms
import httpx
from django.conf import settings
from django.core.exceptions import ValidationError


class HCaptchaField(forms.Field):
    def clean(self, value):
        value = super().clean(value)
        res = httpx.post('https://hcaptcha.com/siteverify',
                         data={
                             'response': value,
                             'secret': settings.HCAPTCHA_SECRET,
                             'sitekey': settings.HCAPTCHA_SITEKEY
                         }
                         )
        result = res.json()
        if not result['success']:
            raise ValidationError('hcaptcha validation error')
        return value


class ImageUploadForm(forms.Form):
    hcaptcha = HCaptchaField()
    image_file = forms.FileField(
        label='Image File',
        widget=forms.FileInput(
            attrs={
                'accept': 'image/jpeg,image/gif,image/png,image/webp',
                'class': 'form-control'
            }
        )
    )
