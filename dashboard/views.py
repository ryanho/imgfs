from django.shortcuts import render
from django.views.generic import ListView
from backend.models import UploadImage, ThumbnailImage
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from customauth.models import User

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


class UserListView(ListView):
    model = User
    template_name = 'dashboard/user_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'dashboard/components/_partial_user_list.html'
        return super().get(request, *args, **kwargs)
