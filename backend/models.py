from django.db import models
from customauth.models import User
from django.utils import timezone

# Create your models here.


class AbstractImageModel(models.Model):
    cid = models.CharField(verbose_name='ipfs cid', max_length=46, primary_key=True)
    filename = models.CharField(verbose_name='filename', max_length=1024)
    width = models.PositiveIntegerField(verbose_name='image width', null=True)
    height = models.PositiveIntegerField(verbose_name='image height', null=True)
    size = models.PositiveIntegerField(verbose_name='file size', null=True)
    content_type = models.CharField(verbose_name='content type', max_length=1024)
    created = models.DateTimeField(verbose_name='created date', default=timezone.now, editable=False)

    class Meta:
        abstract = True


class UploadImage(AbstractImageModel):
    user = models.ManyToManyField(User, verbose_name='user', blank=True)

    class Meta:
        verbose_name = 'Upload image'
        verbose_name_plural = 'Upload images'


class ThumbnailImage(AbstractImageModel):
    origin = models.OneToOneField(UploadImage, verbose_name='origin image', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Thumbnail image'
        verbose_name_plural = 'Thumbnail images'
