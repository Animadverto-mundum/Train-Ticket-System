from flask import redirect, render_template
from . import manager_bp
from model import db, TrainNumber, Line

@manager_bp.route('/train_view')
def train_view():
    trains = db.session.query(TrainNumber).filter().all()
    lists = db.session.query(Line).filter().all()
    dict = {item.line_ID: item.line_name for item in lists}
    return render_template('manage_train_table.html', trains = trains, dict = dict)

@manager_bp.route('/train_edit')
def train_edit():
    return render_template('manage_train_form.html')