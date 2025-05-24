import string

from django.db import models

from home_user.models import User

from common.models import TimeStampMixin

class Tag(models.Model):
    name = models.CharField(max_length=256, unique=True, error_messages={"unique": "tag already exists"})
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return self.name
    
class Folder(TimeStampMixin):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, default=None)
    name = models.CharField(max_length=256)

    def clean(self):
        self.name = self.name.lower()
        return super().clean()

    @property
    def path(self) -> str:
        return f"{self.parent}/{self.name}" if self.parent is not None else f"{self.name}"

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        unique_together = (('parent', 'name'),)

class File(TimeStampMixin):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, blank=True, null=True, default=None)
    file_name = models.CharField(max_length=256, blank=True)
    file_ext = models.CharField(max_length=32)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    # Tags
    tags = models.ManyToManyField(Tag, related_name="files")

    def clean(self):
        self.file_name = self.file_name.lower()
        self.file_ext = self.file_ext.lower()
        return super().clean()

    @property
    def path(self) -> str:
        return f"{self.folder.path}/{self.file_name}.{self.file_ext}" if self.folder is not None else f"{self.file_name}.{self.file_ext}"

    def __str__(self) -> str:
        return f"{self.file_name}.{self.file_ext}"
    
    class Meta:
        unique_together = (('folder', 'file_name', 'file_ext'),)
    
class Person(Tag):
    thumbnail = models.ForeignKey(File, on_delete=models.SET_NULL, blank=True, null=True, default=None)

    def save(self):
        self.name = string.capwords(self.name.strip())
        return super().save()

    def __str__(self) -> str:
        return "%s (Person)" % self.name