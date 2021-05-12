from flask import redirect, render_template, request
from . import manager_bp
from model import db, User
from .manager_auth import login_required

@manager_bp.route('/user_view')
@login_required
def user_view():
    users = User.query.filter().all()
    return render_template('manage_user_table.html', users=users)

@manager_bp.route('user_edit')
def user_edit():
    # user = User.query.filter(User.user_ID==id).first()
    return render_template('manage_user_form.html')

@manager_bp.route('user_edit_single', methods=['GET','POST'])
def user_edit_single():
    error = None
    user = None
    if request.method == 'GET':
        user_id = request.args.get('id')
        user = User.query.filter(User.user_ID==user_id).first()
    elif request.method == 'POST':
        new_username = request.form['user_name']
        password1 = request.form['password1']
        password2 = request.form['password2']
        identity = request.form['identity']
        if password1 != password2:
            error = 'password inconsistent'
        elif User.query.filter(User.user_name==new_username).first() is not None:
            error = f'User {new_username} already exist.'
        if error:
            new_user = User.query.filter(User.user_name==user.user_name).update({
                "user_name":new_username, 
                "password":password1, 
                "user_type_number":identity})
            db.session.commit()
            return redirect(url_for('manager_bp.user_view'))
        flash(error)
    return render_template('manage_user_form.html', user=user)