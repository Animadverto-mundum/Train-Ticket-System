from flask import redirect, render_template
from . import manager_bp

@manager_bp.route('/ticket_view')
def ticket_view():
    return render_template('manage_ticket_table.html')

@manager_bp.route('/ticket_edit')
def ticket_edit():
    return render_template('manage_ticket_form.html')