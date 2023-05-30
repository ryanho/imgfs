from django.conf import settings


def site_settings(request):
    return {'hcaptcha_sitekey': settings.HCAPTCHA_SITEKEY}
