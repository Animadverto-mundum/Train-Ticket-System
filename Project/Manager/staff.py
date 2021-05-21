from flask import redirect, render_template, request, flash, url_for
from . import manager_bp, access_check
from model import db, User, TicketsSold, FareInformation, Line, TrainNumber, UserStaff
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码


identity_switch = {0:'线路管理', 1:'车站管理', 2:'票务管理', 3:'列车管理', 4:'普通用户管理', 5:'超级管理员'}

@manager_bp.route('/staff_view')
@access_check(request)
def staff_view():
    '''查看所有管理員'''
    users = UserStaff.query.filter().all()
    identity = {}
    for user in users:
        identity[user] = identity_switch[user.department_type_number]
    render_args = {
        'users': users, 
        'identity': identity
        }
    user_name = request.cookies.get('user_name')
    return render_template('manage_staff_table.html',**render_args, user_name=user_name)


@manager_bp.route('/staff_add', methods=['POST','GET'])
@access_check(request)
def staff_add():
    '''增加新的普通用户'''
    error = None
    if request.method == 'POST':
        # 获取表单数据
        new_username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        identity = eval(request.form.get('identity'))
        # 处理错误
        if password1 != password2:
            error = 'password inconsistent'
        elif UserStaff.query.filter(UserStaff.user_name == new_username).first() is not None:
            error = f'Staff {new_username} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = UserStaff(user_name=new_username, password=generate_password_hash(password1), department_type_number=identity)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('manager_bp.staff_view'))
        flash(error)
    user_name = request.cookies.get('user_name')
    return render_template('manage_staff_form.html', user=None, type='add', user_name=user_name)

@manager_bp.route('/staff_edit_single', methods=['GET','POST'])
@access_check(request)
def staff_edit_single():
    '''对单个的普通用户进行修改'''
    error = None
    user_name = request.args.get('name')
    user = UserStaff.query.filter(UserStaff.user_name == user_name).first()  # 查找当前修改的用户
    if request.method == 'POST':
        # 获取表单数据
        password1 = request.form['password1']
        password2 = request.form['password2']
        identity = eval(request.form.get('identity'))
        # 处理错误
        if password1 != password2:
            error = 'password inconsistent'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = UserStaff.query.filter(UserStaff.user_name == user_name).update({
                "password": generate_password_hash(password1),
                "department_type_number": identity})
            db.session.commit()
            return redirect(url_for('manager_bp.staff_view'))  # 重定向到普通用户查看页面
        # 将错误放在flash中
        flash(error)
    user_name = request.cookies.get('user_name')
    return render_template('manage_staff_form.html', user=user, type='edit', user_name=user_name)


@manager_bp.route('/staff_delete', methods=["GET"])
@access_check(request)
def staff_delete():
    '''删除单个普通用户'''
    user_name = request.args.get('name')
    user = UserStaff.query.filter(UserStaff.user_name == user_name).first()  # 查找当前修改的用户
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manager_bp.staff_view'))
