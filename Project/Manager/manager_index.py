from flask import render_template, redirect, url_for, session
from . import manager_bp


@manager_bp.route('/index')
def manager_index():
    return render_template('manage_index.html')

@manager_bp.route('/logout')
def manager_logout():
    session.clear()
    return redirect(url_for('manager_bp.manager_auth'))