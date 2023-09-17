import posixpath
from pathlib import Path

from typing import Type, TypeVar, Union

from django.conf import settings
from django.db.models import Model, Q
from django.utils._os import safe_join

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
