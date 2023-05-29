from django.shortcuts import render
from django.views.generic import ListView
from backend.models import UploadImage, ThumbnailImage
from django.conf import settings

# Create your views here.


class ImageListView(ListView):
    model = UploadImage
    template_name = 'dashboard/home.html'
    extra_context = {
        'gateway': settings.IPFS_GATEWAY
    }
