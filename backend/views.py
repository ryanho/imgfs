from django.shortcuts import render, HttpResponse
from django.views.generic import TemplateView
from django.conf import settings
import httpx

# Create your views here.


class HomeView(TemplateView):
    template_name = 'backend/home.html'


class ShowImageView(TemplateView):
    template_name = 'backend/show_image.html'

    def get_context_data(self, **kwargs):
        file_url = f'https://cloudflare-ipfs.com/ipfs/{kwargs.get("cid")}'
        res = httpx.get(file_url)

        context = super().get_context_data(**kwargs)
        context['file_url'] = file_url
        context['content_type'] = res.headers.get('Content-Type')
        return context


def get_image(request, cid, filename):
    gateway = settings.IPFS_GATEWAY
    res = httpx.get(f'{gateway}/ipfs/{cid}?filename={filename}')
    if res.status_code == 200:
        return HttpResponse(res.read(), content_type=res.headers.get('Content-Type'))
    else:
        return HttpResponse(res.content, status=res.status_code)
