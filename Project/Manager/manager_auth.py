import functools
from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import db, UserStaff
from . import manager_bp
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码

@manager_bp.route('/auth', methods=['GET', 'POST'])
def manager_auth():
    if request.method == 'POST':
        if request.form['submit'] == 'Sign In':
            login_username = request.form['login_username']
            login_password = request.form['login_password']
            login_error = None
            login_user = UserStaff.query.filter(UserStaff.user_name == login_username).first()

            if login_user is None:
                login_error = 'Incorrect username'
            elif not check_password_hash(login_user.password, login_password):
                login_error = 'Incorrect password'

            if login_error is None:
                session.clear()
                session['user_ID'] = login_user.staff_ID
                return redirect(url_for('manager_bp.manager_index'))

            flash(login_error, 'login')

        elif request.form['submit'] == 'Sign Up':
            reg_username = request.form['register_username']
            reg_password1 = request.form['register_password1']
            reg_password2 = request.form['register_password2']
            reg_error = None

            if reg_password1 != reg_password2:
                reg_error = 'Inconsistent password.'
            elif reg_username is None:
                reg_error = 'Username is required.'
            elif UserStaff.query.filter(UserStaff.user_name == reg_username).first() is not None:
                reg_error = 'User {} is already registered.'.format(reg_username)

            if reg_error is None:
                reg_user = UserStaff(user_name=reg_username, password=generate_password_hash(reg_password1), department_type_number=1)
                db.session.add(reg_user)
                db.session.commit()
                session.clear()
                session['user_ID'] = UserStaff.query.filter(UserStaff.user_name==reg_username).first().staff_ID
                return redirect(url_for('manager_bp.manager_index'))

            flash(reg_error, 'register')

    return render_template('manage_login_register.html')


@manager_bp.before_app_request
def load_logged_in_user():
    user_ID = session.get('user_ID')
    if user_ID is None:
        g.user = None
    else:
        g.user = UserStaff.query.filter(UserStaff.staff_ID == user_ID).first()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('manager_bp.manager_auth'))
        
        return view(**kwargs)
    
    return wrapped_view
