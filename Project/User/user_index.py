from flask import request, redirect, render_template, url_for, session
from . import user_bp
from config import *
from model import *
from . import access_check
import os
import time


@user_bp.route('/index')
def user_index():
    user_name = request.cookies.get('customer_name')
    image_path = None
    if user_name is not None:
        basedir = os.path.dirname(__file__)
        image_path = 'static/image/' + user_name + '.jpg'
    render_args={
        'user_name':user_name,
        'image_path':image_path
    }           
    return render_template('user_index.html', **render_args, vall=str(time.time()))


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
    error = None
    if request.method == 'POST':
        user_type = request.form.get('browser')
        password1 = request.form['password1']
        password2 = request.form['password2']

        if password1 != password2:
            error = 'inconsistent password!'
        
        if error is None:
            user.password = password1
            if request.files:
                image = request.files['image']
                basedir = os.path.dirname(__file__)
                image_path = os.path.join(basedir,'static','image',reg_username+'.jpg')
                image.save(image_path)
            db.session.commit()

    render_args = {
        'user':user,
        'image_path':'static/image/' + request.cookies.get('customer_name') + '.jpg'
    }
    return render_template('information.html', **render_args, vall=str(time.time()))


@user_bp.route('/3d_show')
@access_check(request)
def user_3dshow():
    render_args = {
        'user_name': request.cookies.get('customer_name'),
        'image_path': 'static/image/' + request.cookies.get('customer_name') + '.jpg' 
    }
    return render_template('3d_show.html', **render_args, vall=str(time.time()))