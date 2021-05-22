import functools
from flask import Blueprint, url_for, redirect


def access_check(request):
    def deco_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.cookies.get("customer_id") and request.cookies.get("customer_name"):
                    ret = True
                else:
                    ret = False
            except:
                ret = False
            if ret:
                return func(*args, **kwargs)
            else:
                response = redirect(url_for('user_bp.user_login'))
                response.delete_cookie('customer_id')
                response.delete_cookie('customer_name')
                return response
        return wrapper
    return deco_func


user_bp = Blueprint('user_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/user')


from . import user_auth, user_index,buyticket,checkticket,refundticket


if __name__ == '__main__':
    pass
