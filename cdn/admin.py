from django.contrib import admin

from cdn.models import *

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass