from flask import render_template, redirect, url_for, session, request
from . import manager_bp, access_check
import random


@manager_bp.route('/index')
def manager_index():
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    user_name = request.cookies.get('user_name')
    return render_template('manage_index.html', user_name=user_name)


@manager_bp.route('/logout')
def manager_logout():
    session.clear()
    response = redirect(url_for('manager_bp.manager_auth'))
    response.delete_cookie("user_name")
    response.delete_cookie("user_type")
    return response
