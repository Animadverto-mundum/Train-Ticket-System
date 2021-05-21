from flask import redirect, render_template, request, url_for
from model import Line, TrainNumber, db, Train, Line

from . import access_check, manager_bp


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
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_index'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    train_list = db.session.query(Train).all()
    line_list = db.session.query(Line).all()
    render_args = {
        'train_list': train_list,
        'line_list': line_list,
        'user_name': request.cookies.get('user_name')
    }
    return render_template('manage_train_form.html', **render_args)


@manager_bp.route('/train_add', methods=['POST'])
def train_add():
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_index'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    
    train_number_ID = request.form.get('train_number_ID')
    train_ID = request.form.get('train_ID')
    line_ID = request.form.get('line_ID').split('-')[0]
    departure_time = request.form.get('departure_time') + ':00'
    arrival_time = request.form.get('arrival_time') + ':00'
    new_train = TrainNumber(train_number_ID=train_number_ID.strip(), train_ID=int(train_ID),\
        line_ID=int(line_ID), departure_time=departure_time, arrival_time=arrival_time)
    db.session.add(new_train)
    db.session.commit()

    return redirect(url_for("manager_bp.train_view"))
