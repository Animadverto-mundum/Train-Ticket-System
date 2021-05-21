import functools
from flask import Blueprint, url_for, redirect


def access_check(request, required_type=''):
    def deco_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.cookies.get("user_id"):
                    ret = True
                else:
                    ret = False
            except:
                ret = False
            if ret:
                return func(*args, **kwargs)
            else:
                response = redirect(url_for('user_bp.user_auth'))
                response.delete_cookie('user_id')
                return response
        return wrapper
    return deco_func

user_bp = Blueprint('user_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/user')


from . import user_auth, user_index,buyticket,checkticket,refundticket


if __name__ == '__main__':
    pass
