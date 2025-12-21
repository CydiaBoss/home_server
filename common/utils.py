import mimetypes, posixpath
from pathlib import Path

from typing import Type, TypeVar, Union

from django.conf import settings
from django.db.models import Model, Q
from django.utils._os import safe_join

from rest_framework.request import Request

# Django Model TypeVar
T = TypeVar("T", bound=Model)

def get_or_none(model : Type[T], *args : Q, **kwargs) -> Union[T, None]:
    """
    Retrieves the first model in a database

    Args:
        model: Django Model
        *args: Q filters
        **Kwargs: Regular filters

    Returns:
        A Django model or None
    """
    return model.objects.filter(*args, **kwargs).first()

def get_filepath(path : str) -> Path:
    """
    Retrieves the path object of a static file

    Args:
        path: Filepath of file within MEDIA_ROOT

    Returns:
        A Filepath object of the file
    """
    path = posixpath.normpath(path).lstrip("/")
    return Path(safe_join(settings.MEDIA_ROOT, path))

def get_media_types() -> tuple[list[str], list[str]]:
    """
    Retrieves the media types from the settings

    Returns:
        A list of media types
    """

    # Media Types
    MEDIA_MIMETYPES = []
    MEDIA_EXT = []
    mimetypes.init()
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] in ("video", "audio", "image"):
            MEDIA_MIMETYPES.append(mimetypes.types_map[ext].lower())
            MEDIA_EXT.append(ext[1:])

    return MEDIA_MIMETYPES, MEDIA_EXT

def get_client_ip(request : Request) -> str:
    """
    Retrieves the client's IP address from the request object.
    """
    # Check if the request went through a proxy or load balancer
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        # The real IP is usually the last one in the list
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        # Fallback to the direct connection IP
        ip = request.META.get('REMOTE_ADDR')
    return ip