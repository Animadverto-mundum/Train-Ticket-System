import functools
from flask import Blueprint, url_for, redirect

def access_check(request, required_type=''):
    def deco_func(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if request.cookies.get("user_name") and request.cookies.get("user_type") in '0' + str(required_type):
                    ret = True
                else:
                    ret = False
            except:
                ret = False
            if ret:
                return func(*args, **kwargs)
            else:
                response = redirect(url_for('manager_bp.manager_auth'))
                response.delete_cookie('user_name')
                response.delete_cookie('user_type')
                return response
        return wrapper
    return deco_func

manager_bp = Blueprint('manager_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/manager')

from . import manager_auth, manager_index, route, station, ticket, train, user, staff

if __name__=='__main__':
    pass