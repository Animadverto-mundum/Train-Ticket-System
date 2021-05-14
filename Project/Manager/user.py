from flask import redirect, render_template, request, flash, url_for
from . import manager_bp
from model import db, User
from .manager_auth import login_required
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码


@manager_bp.route('/user_view')
@login_required
def user_view():
    '''查看所有普通用户'''
    users = User.query.filter().all()
    return render_template('manage_user_table.html', users=users)


@manager_bp.route('user_add', methods=['POST','GET'])
@login_required
def user_add():
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
        elif User.query.filter(User.user_name==new_username).first() is not None:
            error = f'User {new_username} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = User(user_name=new_username, password=generate_password_hash(password1), user_type_number=identity)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('manager_bp.user_view'))
        flash(error)

    return render_template('manage_user_form.html', user=None)


@manager_bp.route('user_edit_single', methods=['GET','POST'])
@login_required
def user_edit_single():
    '''对单个的普通用户进行修改'''
    error = None
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID==user_id).first() # 查找当前修改的用户
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
        elif User.query.filter(User.user_name==new_username).first() is not None:
            error = f'User {new_username} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_user = User.query.filter(User.user_name==user.user_name).update({
                "user_name":new_username, 
                "password":generate_password_hash(password1), 
                "user_type_number":identity})
            db.session.commit()
            return redirect(url_for('manager_bp.user_view')) # 重定向到普通用户查看页面
        # 将错误放在flash中
        flash(error)
    return render_template('manage_user_form.html', user=user)


@manager_bp.route('user_delete', methods=["GET"])
@login_required
def user_delete():
    '''删除单个普通用户'''
    user_id = request.args.get('id')
    user = User.query.filter(User.user_ID==user_id).first() # 查找当前删除的普通用户

    db.session.delete(user)
    db.session.commit()

    return redirect(url_for('manager_bp.user_view'))