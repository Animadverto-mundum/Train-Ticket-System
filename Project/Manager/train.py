from flask import redirect, render_template
from . import manager_bp

@manager_bp.route('/train_view')
def train_view():
    return render_template('manage_train_table.html')

@manager_bp.route('/train_edit')
def train_edit():
    return render_template('manage_train_form.html')