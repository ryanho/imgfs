from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from backend.models import UploadImage, ThumbnailImage
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from customauth.models import User
import httpx
import logging

# Create your views here.


class ImageListView(LoginRequiredMixin, ListView):
    model = UploadImage
    template_name = 'dashboard/home.html'
    extra_context = {
        'gateway': settings.IPFS_GATEWAY
    }
    ordering = ['-created']
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related('thumbnailimage')

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'dashboard/components/_partial_image_list.html'
        return super().get(request, *args, **kwargs)


class DeleteImageView(LoginRequiredMixin, DeleteView):
    model = UploadImage
    success_url = reverse_lazy('ImageListView')

    def form_valid(self, form):
        api = settings.IPFS_API + '/api/v0'
        with httpx.Client() as client:
            # delete thumbnail
            url = f'{api}/pin/rm?arg={self.object.thumbnailimage.cid}'
            res = client.post(url)
            if res.status_code == 200:
                self.object.thumbnailimage.delete()
                logging.info(f'delete thumbnail {self.object.thumbnailimage.cid}')

            # delete image
            url = f'{api}/pin/rm?arg={self.object.cid}'
            res = client.post(url)
            if res.status_code == 200:
                self.object.delete()
                logging.info(f'delete image {self.object.cid}')

            # ipfs gc
            url = f'{api}/repo/gc'
            res = client.post(url)
            if res.status_code == 200:
                print(res.text)
            return redirect('ImageListView')


class UserListView(ListView):
    model = User
    template_name = 'dashboard/user_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'dashboard/components/_partial_user_list.html'
        return super().get(request, *args, **kwargs)
