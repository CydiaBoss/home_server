from django.contrib import admin

from home_user.models import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(UserSetting)
class UserSettingsAdmin(admin.ModelAdmin):
    pass