from django.db import models

from home_user.models import User

from common.models import TimeStampMixin

from .settings import *

class MediaMixin(TimeStampMixin):
    file_name = models.CharField(max_length=256)
    file_ext = models.CharField(max_length=32)
    file = models.FileField(upload_to=DEFAULT_DIRECTORY)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    class Meta:
        abstract = True

class Photo(MediaMixin):
    file = models.ImageField(upload_to=PHOTO_DIRECTORY)

class Video(MediaMixin):
    file = models.FileField(upload_to=VIDEO_DIRECTORY)