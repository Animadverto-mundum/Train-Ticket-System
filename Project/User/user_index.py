from flask import render_template, redirect, url_for, session
from . import user_bp
from .user_auth import login_required


@user_bp.route('/index')
@login_required
def user_index():
    return render_template('user_index.html')


@user_bp.route('/logout')
@login_required
def user_logout():
    session.clear()
    return redirect(url_for('user_bp.user_login'))