from flask import redirect, render_template
from . import manager_bp
from model import db, TrainNumber

@manager_bp.route('/train_view')
def train_view():
    lines = db.session.query.filter().all()
    lists = db.session.query.filter().all()
    dict = {item.line_ID: item.line_name for item in lists}
    return render_template('manage_train_table.html', {'lines': lines, 'dict': dict})

@manager_bp.route('/train_edit')
def train_edit():
    return render_template('manage_train_form.html')