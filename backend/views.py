from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.conf import settings
import httpx
from .forms import ImageUploadForm, GuestImageUploadForm
import json
from easy_thumbnails.files import Thumbnailer
from .models import UploadImage, ThumbnailImage
from customauth.models import User

# Create your views here.


class HomeView(FormView):
    template_name = 'backend/home.html'
    form_class = GuestImageUploadForm

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'backend/components/_partial_home.html'
        return super().get(request, *args, **kwargs)

    def get_form_class(self):
        if self.request.user.is_authenticated:
            return ImageUploadForm
        else:
            return super().get_form_class()

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

    @staticmethod
    def upload_file(img_file):
        url = f'{settings.IPFS_API}/api/v0/add'
        files = {'file': (img_file.name, img_file.file)}
        res = httpx.post(
            url,
            files=files,
        )
        result = json.loads(res.content.decode('utf8'))
        return result

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = None

        img_file = form.files['image_file']
        result = self.upload_file(img_file)
        cid = result['Hash']

        image, created = UploadImage.objects.get_or_create(
            cid=cid,
            defaults={
                'user': user, 'filename': img_file.name, 'width': img_file.image.width, 'height': img_file.image.height,
                'size': result['Size'], 'content_type': img_file.image.get_format_mimetype()
            }
        )

        if created:
            return redirect(
                reverse('ShowImageView', kwargs={'cid': cid})
            )

        thumbnailer = Thumbnailer(img_file)
        thumbnail = thumbnailer.generate_thumbnail({'size': (540, 540)})
        result = self.upload_file(thumbnail)

        thumb_image = ThumbnailImage(
            origin=image, cid=result['Hash'], filename=thumbnail.name, width=thumbnail.image.width,
            height=thumbnail.image.height, size=result['Size'], content_type=img_file.image.get_format_mimetype()
        )
        thumb_image.save()

        return redirect(
            reverse('ShowImageView', kwargs={'cid': cid})
        )


class ShowImageView(TemplateView):
    template_name = 'backend/show_image.html'

    def get_context_data(self, **kwargs):
        cid = kwargs.get("cid")
        image = get_object_or_404(UploadImage, cid=cid)

        context = super().get_context_data(**kwargs)
        context['imgurl'] = reverse('GetImage', kwargs={'cid': cid, 'filename': image.filename})
        context['file_url'] = f'{settings.IPFS_GATEWAY}/ipfs/{image.thumbnailimage.cid}'
        context['image'] = image
        return context

    def get(self, request, *args, **kwargs):
        if request.htmx:
            self.template_name = 'backend/components/_partial_show_image.html'
        return super().get(request, *args, **kwargs)


def get_image(request, cid, filename):
    image = get_object_or_404(UploadImage, cid=cid)
    gateway = settings.IPFS_GATEWAY
    res = httpx.get(f'{gateway}/ipfs/{cid}?filename={filename}', timeout=60)

    headers = {
        'Cache-Control': res.headers.get('Cache-Control'),
        'Etag': res.headers.get('Etag')
    }

    if res.status_code == 200:
        return HttpResponse(res.read(), content_type=image.content_type, headers=headers)
    else:
        return HttpResponse(res.content, status=res.status_code)
