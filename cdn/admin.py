from django.contrib import admin

from cdn.models import *

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    pass

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    pass

@admin.register(VideoDetail)
class VideoDetailAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    pass

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    pass

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass