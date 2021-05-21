from flask import redirect, render_template, request, flash, url_for
from . import manager_bp, access_check
from model import db, User, TicketsSold, FareInformation, Line, TrainNumber
# from .manager_auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码
import random


@manager_bp.route('/user_view')
def user_view():
    '''查看所有普通用户'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    users = User.query.filter().all()
    user_name = request.cookies.get('user_name')
    return render_template('manage_user_table.html', users=users, user_name=user_name)


@manager_bp.route('/user_add', methods=['POST','GET'])
def user_add():
    '''增加新的普通用户'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    error = None
    if request.method == 'POST':
        # 获取表单数据
        new_username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if request.form.get('identity') == 'student':
            identity = 1
        else:
            identity = 0
        # 处理错误
        if password1 != password2:
            error = 'password inconsistent'
        elif User.query.filter(User.user_name == new_username).first() is not None:
            error = f'User {new_username} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = User(user_name=new_username, password=generate_password_hash(password1), user_type_number=identity)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('manager_bp.user_view'))
        flash(error)
    user_name = request.cookies.get('user_name')
    return render_template('manage_user_form.html', user=None, user_name=user_name)


@manager_bp.route('/user_edit_single', methods=['GET','POST'])
def user_edit_single():
    '''对单个的普通用户进行修改'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    error = None
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID == user_id).first()  # 查找当前修改的用户
    if request.method == 'POST':
        # 获取表单数据
        new_username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        if request.form.get('identity') == 'student':
            identity = 1
        else:
            identity = 0
        # 处理错误
        if password1 != password2:
            error = 'password inconsistent'
        elif User.query.filter(User.user_name == new_username).first() is not None:
            error = f'User {new_username} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = User.query.filter(User.user_name == user.user_name).update({
                "user_name": new_username,
                "password": generate_password_hash(password1),
                "user_type_number": identity})
            db.session.commit()
            return redirect(url_for('manager_bp.user_view'))  # 重定向到普通用户查看页面
        # 将错误放在flash中
        flash(error)
    user_name = request.cookies.get('user_name')
    return render_template('manage_user_form.html', user=user, user_name=user_name)


@manager_bp.route('/user_delete', methods=["GET"])
def user_delete():
    '''删除单个普通用户'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID == user_id).first()  # 查找当前删除的普通用户
    db.session.delete(user)
    db.session.commit()

    user_name = request.cookies.get('user_name')
    return redirect(url_for('manager_bp.user_view'))


@manager_bp.route('/user_view_single', methods=["GET"])
def user_view_single():
    '''查看单个用户的购票信息'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID==user_id).first() # 查找当前查看的用户
    # 查询该用户的购票信息
    tickets = db.session.query(TicketsSold.seat, TrainNumber.train_number_ID, Line.line_name, FareInformation.money, FareInformation.seat_type, TrainNumber.departure_time, TrainNumber.arrival_time, TicketsSold.departure_date).filter(
        Line.line_ID==TrainNumber.line_ID,
        TicketsSold.user_ID==user.user_ID,
        TicketsSold.fare_ID==FareInformation.fare_ID, 
        FareInformation.train_number_id==TrainNumber.train_number_ID)
    user_name = request.cookies.get('user_name')
    return render_template('manage_user_viewsingle.html', user=user, tickets=tickets, user_name=user_name)
