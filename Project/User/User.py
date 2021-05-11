from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from werkzeug.security import check_password_hash, generate_password_hash  # 避免数据库中直接存储密码

user_app = Blueprint('user_app', __name__, static_folder='static', template_folder='templates', url_prefix='/user')

@user_app.route('/user_login', methods=['GET', 'POST'])
def user_login():

    return render_template('user_login.html')

@user_app.route('/user_register', methods=['GET', 'POST'])
def user_register():

    return render_template('user_register.html')

@user_app.route('/user_index', methods=['GET', 'POST'])
def user_index():

    return render_template('user_index.html')

@user_app.route('/user_buyTicket', methods=['GET', 'POST'])
def user_buyticket():

    return render_template('user_buyTicket.html')

@user_app.route('/user_checkTicket', methods=['GET', 'POST'])
def user_checkticket():

    return render_template('user_checkTicket.html')

@user_app.route('/user_refundTicket', methods=['GET', 'POST'])
def user_refundticket():

    return render_template('user_refundTicket.html')
