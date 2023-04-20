from functools import wraps
from flask_login import current_user
from flask import flash, redirect, url_for,abort


def seller_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'seller': # type: ignore
            abort(403) # Forbidden
        return func(*args, **kwargs)
    return decorated_view