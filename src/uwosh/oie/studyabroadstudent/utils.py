from functools import wraps
from plone.api.env import adopt_roles


def with_manager_permissions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with adopt_roles(['Manager']):
            func(*args, **kwargs)
    return wrapper
