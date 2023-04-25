from django.contrib import admin

from media.models import *

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    pass