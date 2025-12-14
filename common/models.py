from django.db import models

# Create your models here.
class TimeStampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Languages(models.TextChoices):
    EN = "EN", "English"
    FR = "FR", "French"
    ZH_CN = "ZH_CN", "Chinese (Simplified)"
    ZH_TW = "ZH_TW", "Chinese (Traditional)"