from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from . import user_bp
from .user_auth import login_required
from config import *
from model import *
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码
from . import access_check


@user_bp.route('/index')
def user_index():
    user_name = request.cookies.get('customer_name')
    return render_template('user_index.html', user_name=user_name)


@user_bp.route('/logout')
def user_logout():
    session.clear()
    response = redirect(url_for('user_bp.user_login'))
    response.delete_cookie('customer_id')
    response.delete_cookie('customer_name')
    return response

@user_bp.route('/information',methods=['GET', 'POST'])
def user_infomation():
    reg_username = request.cookies.get('customer_name')
    user=User.query.filter(User.user_name == reg_username).first()
    if request.method == 'POST':
        user_type = request.form.get('browser')
        avatar = request.files.get('avatar') # 读取
        if avatar is not None:
            fname = avatar.filename

            if ('.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS):
                avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, reg_username, fname))
                path_avatar = '{}{}_{}'.format(UPLOAD_FOLDER_SAVE, reg_username, fname)
                user.avatar_path=path_avatar
            else:
                error = '头像格式错误'
                flash(error, 'touxiang')
                return redirect(url_for('user_bp.user_infomation'))

        if user_type is not None:
            user.user_type_number=user_type
            print("修改用户类型")

        db.session.commit()

    return render_template('information.html',user=user)


@user_bp.route('/3d_show')
def user_3dshow():
    return render_template('3d_show.html', user_name=request.cookies.get('customer_name'))