from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from Project.model import *
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码

auth_app = Blueprint('auth_app', __name__, static_folder='static', template_folder='templates', url_prefix='/auth')


@auth_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if username is None:
            error = 'Username is required.'
        elif password is None:
            error = 'Password is required.'
        elif User.query.filter(User.user_name == username).first() is not None:
            error = 'User {} is already registered.'.format(username)

        if error is None:
            user = User(user_name=username, password=generate_password_hash(password), user_type_number=1)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('auth_app.login'))

        flash(error)

    return render_template('register.html')


@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.user_name == username).first()

        if user is None:
            error = 'Incorrect username'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password'

        if error is None:
            session.clear()
            session['user_ID'] = user.user_ID
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


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
