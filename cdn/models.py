from django.db import models

from home_user.models import User

from common.models import TimeStampMixin

class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True, error_messages={"unique": "tag already exists"})
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.name

class File(TimeStampMixin):
    file_name = models.CharField(max_length=256)
    file_ext = models.CharField(max_length=32)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    # Tags
    tags = models.ManyToManyField(Tag, related_name="files")

    def __str__(self) -> str:
        return f"{self.file_name}.{self.file_ext}"