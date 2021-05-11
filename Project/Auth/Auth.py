from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码

auth_app = Blueprint('auth_app', __name__, static_folder='../static', template_folder='../templates', url_prefix='/auth')


@auth_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if request.form['submit'] == 'Sign Up':
            reg_username = request.form['register_username']
            reg_password1 = request.form['register_password1']
            reg_password2 = request.form['register_password2']
            reg_error = None

            if reg_password1 != reg_password2:
                reg_error = 'Inconsistent password.'
            elif reg_username is None:
                reg_error = 'Username is required.'
            elif User.query.filter(User.user_name == reg_username).first() is not None:
                reg_error = 'User {} is already registered.'.format(reg_username)

            if reg_error is None:
                reg_user = User(user_name=reg_username, password=generate_password_hash(reg_password1), user_type_number=1)
                db.session.add(reg_user)
                db.session.commit()
                return redirect(url_for('auth_app.login'))

    return render_template('manage_login_register.html')


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['submit'] == 'Sign In':
            login_username = request.form['login_username']
            login_password = request.form['login_password']
            login_error = None
            login_user = User.query.filter(User.user_name == login_username).first()

            if login_user is None:
                login_error = 'Incorrect username'
            elif not check_password_hash(login_user.password, login_password):
                login_error = 'Incorrect password'

            if login_error is None:
                session.clear()
                session['user_ID'] = login_user.user_ID
                return redirect(url_for('manage_index'))

            flash(login_error)

        elif request.form['submit'] == 'Sign Up':
            reg_username = request.form['register_username']
            reg_password1 = request.form['register_password1']
            reg_password2 = request.form['register_password2']
            reg_error = None

            if reg_password1 != reg_password2:
                reg_error = 'Inconsistent password.'
            elif reg_username is None:
                reg_error = 'Username is required.'
            elif User.query.filter(User.user_name == reg_username).first() is not None:
                reg_error = 'User {} is already registered.'.format(reg_username)

            if reg_error is None:
                reg_user = User(user_name=reg_username, password=generate_password_hash(reg_password1), user_type_number=1)
                db.session.add(reg_user)
                db.session.commit()
                return redirect(url_for('manage_login'))

            flash(reg_error)

    return render_template('manage_login_register.html')


@auth_app.before_app_request
def load_logged_in_user():
    user_ID = session.get('user_ID')
    if user_ID is None:
        g.user = None
    else:
        g.user = User.query.filter(User.user_ID == user_ID).first()


@auth_app.route('logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
