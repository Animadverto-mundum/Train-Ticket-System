from flask import redirect, render_template, request, redirect, url_for
from . import manager_bp, access_check
from model import db, TrainNumber, Line

@manager_bp.route('/train_view')
def train_view():
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_index'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    trains = db.session.query(TrainNumber).filter().all()
    lists = db.session.query(Line).filter().all()
    dict = {item.line_ID: item.line_name for item in lists}

    render_args = {
        'trains': trains, 
        'dict': dict,
        'user_name': request.cookies.get('user_name'),
        }
    return render_template('manage_train_table.html', **render_args)

@manager_bp.route('/train_edit')
def train_edit():
    return render_template('manage_train_form.html')