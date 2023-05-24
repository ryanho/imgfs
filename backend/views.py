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
            reverse('ShowImageView', kwargs={'cid': result['Hash']}) + f'?filename={result["Name"]}'
        )


class ShowImageView(TemplateView):
    template_name = 'backend/show_image.html'

    def get_context_data(self, **kwargs):
        file_url = f'https://cloudflare-ipfs.com/ipfs/{kwargs.get("cid")}'
        res = httpx.get(file_url, timeout=60)

        context = super().get_context_data(**kwargs)
        context['file_url'] = file_url
        context['content_type'] = res.headers.get('Content-Type')
        return context


def get_image(request, cid, filename):
    gateway = settings.IPFS_GATEWAY
    res = httpx.get(f'{gateway}/ipfs/{cid}?filename={filename}', timeout=60)
    if res.status_code == 200:
        return HttpResponse(res.read(), content_type=res.headers.get('Content-Type'))
    else:
        return HttpResponse(res.content, status=res.status_code)
