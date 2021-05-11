from flask import redirect, render_template
from . import manager_bp

@manager_bp.route('/station_view')
def station_view():
    return render_template('manage_station_table.html')

@manager_bp.route('/station_edit')
def station_edit():
    return render_template('manage_station_form.html')