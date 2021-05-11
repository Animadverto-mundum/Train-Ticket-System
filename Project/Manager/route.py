from flask import redirect, render_template
from . import manager_bp

@manager_bp.route('/route_view')
def route_view():
    return render_template('manage_route_table.html')

@manager_bp.route('/route_edit')
def route_edit():
    return render_template('manage_route_form.html')