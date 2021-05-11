from flask import Blueprint 

manager_bp = Blueprint('manage_bp', __name__, static_folder='static', template_folder='templates', url_prefix='/manager')

from . import manager_auth, manager_index

if __name__=='__main__':
    pass