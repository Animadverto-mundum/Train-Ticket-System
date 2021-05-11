from flask import redirect, render_template
from . import manager_bp

@manager_bp.route('/user_view')
def user_view():
    return render_template('manage_user_table.html')

@manager_bp.route('/user_edit')
def user_edit():
    return render_template('manage_user_form.html')