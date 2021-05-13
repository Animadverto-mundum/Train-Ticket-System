from flask import render_template, redirect, url_for, session
from . import manager_bp
from .manager_auth import login_required

@manager_bp.route('/index')
@login_required
def manager_index():
    return render_template('manage_index.html')

@manager_bp.route('/logout')
@login_required
def manager_logout():
    session.clear()
    return redirect(url_for('manager_bp.manager_auth'))