from flask import render_template
from . import manager_bp

@manager_bp.route('/index')
def manager_index():
    return render_template('manage_index.html')