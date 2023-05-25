from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import TemplateView, FormView
from django.conf import settings
import httpx
from .forms import ImageUploadForm
import json

# Create your views here.


class HomeView(FormView):
    template_name = 'backend/home.html'
    form_class = ImageUploadForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hcaptcha_sitekey'] = settings.HCAPTCHA_SITEKEY
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method == 'POST':
            kwargs.update({
                'data': {
                    'hcaptcha': self.request.POST.get('h-captcha-response', None)
                }
            })
        return kwargs

    def form_valid(self, form):
        url = f'{settings.IPFS_API}/api/v0/add'
        img_file = form.files['image_file']
        files = {'file': (img_file.name, img_file.file)}
        res = httpx.post(
            url,
            files=files,
        )
        result = json.loads(res.content.decode('utf8'))
        return redirect(
            reverse('ShowImageView', kwargs={'cid': result['Hash']})
        )


class ShowImageView(TemplateView):
    template_name = 'backend/show_image.html'

    def get_context_data(self, **kwargs):
        cid = kwargs.get("cid")
        file_url = f'{settings.IPFS_GATEWAY}/ipfs/{cid}'
        res = httpx.get(file_url, timeout=60)

        context = super().get_context_data(**kwargs)
        context['file_url'] = file_url
        context['content_type'] = res.headers.get('Content-Type')

        filename = 'share'
        if context['content_type'] == 'image/jpeg':
            filename += '.jpg'
        elif context['content_type'] == 'image/gif':
            filename += '.gif'
        elif context['content_type'] == 'image/png':
            filename += '.png'
        elif context['content_type'] == 'image/webp':
            filename += '.webp'
        else:
            filename = None

        if filename is None:
            context['imgurl'] = None
        else:
            context['imgurl'] = reverse('GetImage', kwargs={'cid': cid, 'filename': filename})
        return context


def get_image(request, cid, filename):
    gateway = settings.IPFS_GATEWAY
    res = httpx.get(f'{gateway}/ipfs/{cid}?filename={filename}', timeout=60)

    headers = {
        'Cache-Control': res.headers.get('Cache-Control'),
        'Etag': res.headers.get('Etag')
    }

    if res.status_code == 200:
        return HttpResponse(res.read(), content_type=res.headers.get('Content-Type'), headers=headers)
    else:
        return HttpResponse(res.content, status=res.status_code)
