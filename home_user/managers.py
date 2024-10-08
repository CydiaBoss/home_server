from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext as _

class HomeUserManager(BaseUserManager):
    """
    Custom user model manager for home_server
    """

    def create_user(self, username, email, password, **extra_fields):
        if not email or not username:
            raise ValueError(_('Users must have a username and an email address'))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, email, password, **extra_fields)