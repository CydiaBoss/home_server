from typing import Type, TypeVar, Union

from django.db.models import Model, Q

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