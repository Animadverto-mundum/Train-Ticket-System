from flask import Blueprint 


def access_check(request, allow_type):
    try:
        if request.cookies.get("user_name") and request.cookies.get("user_type") == str(allow_type):
            return True
        else:
            return False
    except:
        return False


manager_bp = Blueprint('manager_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/manager')

from . import manager_auth, manager_index, route, station, ticket, train, user

if __name__=='__main__':
    pass