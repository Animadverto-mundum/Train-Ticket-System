import functools
from flask import request, redirect, render_template, url_for, session, flash, g
from model import db, User
from . import user_bp
import os


@user_bp.route('/', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        login_error = None
        login_username = request.form['user']
        login_password = request.form['password']
        login_user = User.query.filter(User.user_name == login_username).first()

        login_userid = login_user.user_ID

        if login_user is None:
            login_error = 'User {} does not exist!'.format(login_username)
        elif login_user.password != login_password:
            login_error = 'Incorrect password!'
        
        if login_error is None:
            session.clear()
            session['user_ID'] = login_user.user_ID
            respond = redirect(url_for('user_bp.user_index'))
            respond.set_cookie('customer_id', str(login_userid))
            respond.set_cookie('customer_name', login_username)
            return respond

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
            if request.files:
                image = request.files['image']
                basedir = os.path.dirname(__file__)
                image_path = os.path.join(basedir,'static','image',reg_username+'.jpg')
                image.save(image_path)
            reg_user = User(user_name=reg_username, password=reg_password1, user_type_number=user_type)
            db.session.add(reg_user)
            db.session.commit()
            
            session.clear()
            reg_userid = User.query.filter(User.user_name == reg_username).first().user_ID
            session['user_ID'] = reg_userid
            respond = redirect(url_for('user_bp.user_index'))
            respond.set_cookie('customer_id', str(reg_userid))
            respond.set_cookie('customer_name', reg_username)
            return respond

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
            reg_error = 'User {} does not exist!'.format(reg_username)
        elif reg_password1 != reg_password2:
            reg_error = 'inconsistent password!'
        
        if reg_error is None:
            user.password = reg_password1
            reg_error = 'Successfully change!'
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

