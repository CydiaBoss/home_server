from django.db import models

from common.models import TimeStampMixin

from .settings import *

class MediaMixin(TimeStampMixin):
    file_name = models.CharField(max_length=256)
    file_ext = models.CharField(max_length=32)
    file_path = models.FileField(upload_to=DEFAULT_DIRECTORY)

    class Meta:
        abstract = True

class Photo(models.Model):
    file_path = models.FileField(upload_to=PHOTO_DIRECTORY)

class Video(models.Model):
    file_path = models.FileField(upload_to=VIDEO_DIRECTORY)