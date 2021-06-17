from functools import wraps

from flask import abort
from flask_login import current_user

from model import Role


def has_authority(role):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if Role.query.filter(Role.name == role).first().value <= Role.query.filter(
                    Role.id == current_user.role_id).first().value:
                return func(*args, **kwargs)
            return abort(403)

        return wrapper

    return actual_decorator
