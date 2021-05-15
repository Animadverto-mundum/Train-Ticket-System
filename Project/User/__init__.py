from flask import Blueprint

user_bp = Blueprint('user_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/user')


from . import user_auth, user_index,buyticket,checkticket,refundticket


if __name__ == '__main__':
    pass
