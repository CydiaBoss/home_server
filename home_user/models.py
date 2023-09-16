from rest_framework.authtoken.models import Token

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from common.models import TimeStampMixin

from home_user.managers import HomeUserManager

class User(AbstractBaseUser, PermissionsMixin):
    '''
    User model for the home_server
    '''
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(_("username"), max_length=256, unique=True, validators=[username_validator])
    email = models.EmailField(_("email address"), unique=True)

    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)

    is_staff = models.BooleanField(_("staff status"), default=False)
    is_active = models.BooleanField(_("active"), default=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    objects = HomeUserManager()

    def __str__(self):
        return self.username
    
class UserSession(TimeStampMixin):
    '''
    A User Session model
    '''
    token = models.OneToOneField(Token, on_delete=models.CASCADE, verbose_name=_("authentication token"))
    ip_address = models.GenericIPAddressField(_("ip address"), protocol="IPv4")