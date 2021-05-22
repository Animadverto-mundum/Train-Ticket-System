from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from . import user_bp
from .user_auth import login_required
from config import *
from model import *
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码
from . import access_check


@user_bp.route('/index')
def user_index():
    return render_template('user_index.html')


@user_bp.route('/logout')
def user_logout():
    session.clear()
    response = redirect(url_for('user_bp.user_login'))
    response.delete_cookie('customer_id')
    response.delete_cookie('customer_name')
    return response

@user_bp.route('/information',methods=['GET', 'POST'])
def user_infomation():
    if request.method == 'POST':
        print("搞毛吗",request.values)
        reg_username=g.user.user_name
        user=User.query.filter(User.user_name == reg_username).first()
        # reg_password = request.form.get('password')
        user_type = request.form.get('browser')
        print(user_type)
        avatar = request.files.get('avatar') # 读取
        print("看看头像",avatar)
        if avatar is not None:
            print("进来了")
            fname = avatar.filename

            if ('.' in fname and fname.rsplit('.',1)[1] in ALLOWED_EXTENSIONS):
                avatar.save('{}{}_{}'.format(UPLOAD_FOLDER, reg_username, fname))
                path_avatar = '{}{}_{}'.format(UPLOAD_FOLDER_SAVE, reg_username, fname)
                user.avatar_path=path_avatar
            else:
                error = '头像格式错误'
                flash(error, 'touxiang')
                print("错了")
                return redirect(url_for('user_bp.user_infomation'))
        # if reg_password is not None:
        #     user.password=generate_password_hash(reg_password)
        #     print("密码")

        if user_type is not None:
            user.user_type_number=user_type
            print("修改用户类型")

        db.session.commit()

    return render_template('information.html')


@user_bp.route('/3d_show')
def user_3dshow():
    return render_template('3d_show.html')