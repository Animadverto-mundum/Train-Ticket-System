import functools
from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import db, User
from . import user_bp
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码


@user_bp.route('/', methods=['GET', 'POST'])
def user_login():
    # print(request)
    if request.method == 'POST':
        login_username = request.form['user']
        login_password = request.form['password']
        login_error = None
        login_user = User.query.filter(User.user_name == login_username).first()

        if login_user is None:
            login_error = 'User does not exist!'
        elif not check_password_hash(login_user.password, login_password):
            login_error = 'Incorrect password'
        
        if login_error is None:
            session.clear()
            session['user_ID'] = login_user.user_ID
            return redirect(url_for('user_bp.user_index'))
        flash(login_error, 'login')
    return render_template('user_login.html')


@user_bp.route('/register', methods=['GET', 'POST'])
def user_register():
    print(request.values)
    if request.method == 'POST':
        reg_username = request.form.get('user')
        reg_password1 = request.form.get('password1')
        reg_password2 = request.form.get('password2')

        if request.form.get('browser') == '成人':
            user_type = 0
        else:
            user_type = 1

        reg_error = None

        if reg_password1 != reg_password2:
            reg_error = 'Inconsistent password.'
        elif User.query.filter(User.user_name == reg_username).first() is not None:
            reg_error = 'User {} is already registered.'.format(reg_username)

        if reg_error is None:
            reg_user = User(user_name=reg_username, password=generate_password_hash(reg_password1),
                            user_type_number=user_type)
            db.session.add(reg_user)
            db.session.commit()
            
            session.clear()
            session['user_ID'] = User.query.filter(User.user_name == reg_username).first().user_ID
            return redirect(url_for('user_bp.user_index'))

        flash(reg_error, 'register')

    if request.method=='GET':
        return render_template('user_register.html')
    return render_template('user_register.html')


@user_bp.route('/change_password', methods=['GET', 'POST'])
def user_change_password():
    print(request.values)
    if request.method == 'POST':
        reg_username = request.form.get('user')
        reg_password1 = request.form.get('password1')
        reg_password2 = request.form.get('password2')
        reg_error = None
        user = User.query.filter(User.user_name == reg_username).first()

        if user is None:
            reg_error = '用户不存在！'
        elif reg_password1 != reg_password2:
            reg_error = '两次密码不一致！'
        
        if reg_error is None:
            user.password = generate_password_hash(reg_password2)
            reg_error = '修改成功！'
            flash(reg_error, 'changepassword')
            db.session.commit()
            return redirect(url_for('user_bp.user_login'))

        flash(reg_error, 'changepassword')

    if request.method == 'GET':
        return render_template('user_changepassword.html')

    return render_template('user_changepassword.html')


@user_bp.before_app_request
def load_logged_in_user():
    user_ID = session.get('user_ID')
    if user_ID is None:
        g.user = None
    else:
        g.user = User.query.filter(User.user_ID == user_ID).first()


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('user_bp.user_login'))
        return view(**kwargs)
    return wrapped_view

