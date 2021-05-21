from flask import redirect, render_template, request, flash, url_for
from . import manager_bp
from model import db, User, TicketsSold, FareInformation, Line, TrainNumber
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码


@manager_bp.route('/staff_view')
def staff_view():
    '''查看所有普通用户'''
    users = User.query.filter().all()
    return render_template('manage_user_table.html', users=users)


@manager_bp.route('/staff_add', methods=['POST','GET'])
def staff_add():
    '''增加新的普通用户'''
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

    return render_template('manage_user_form.html', user=None)

@manager_bp.route('/staff_edit_single', methods=['GET','POST'])
def staff_edit_single():
    '''对单个的普通用户进行修改'''
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
    return render_template('manage_user_form.html', user=user)


@manager_bp.route('/staff_delete', methods=["GET"])
def staff_delete():
    '''删除单个普通用户'''
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID == user_id).first()  # 查找当前删除的普通用户
    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manager_bp.user_view'))

@manager_bp.route('/staff_view_single', methods=["GET"])
def staff_view_single():
    '''查看单个用户的购票信息'''
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID==user_id).first() # 查找当前查看的用户
    # 查询该用户的购票信息
    tickets = db.session.query(TicketsSold.seat, TrainNumber.train_number_ID, Line.line_name, FareInformation.money, FareInformation.seat_type, TrainNumber.departure_time, TrainNumber.arrival_time, TicketsSold.departure_date).filter(
        Line.line_ID==TrainNumber.line_ID,
        TicketsSold.user_ID==user.user_ID,
        TicketsSold.fare_ID==FareInformation.fare_ID,
        FareInformation.train_number_id==TrainNumber.train_number_ID)

    return render_template('manage_user_viewsingle.html', user=user, tickets=tickets)
