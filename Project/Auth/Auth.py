from flask import Blueprint, request, redirect, render_template, url_for
from model import *

auth_app = Blueprint('auth_app', __name__, static_folder='static', template_folder='templates', url_prefix='/auth')

@auth_app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(user_name=username, password=password, user_type_number=1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('/login'))
    return render_template('register.html')

@auth_app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter(
            User.user_name == username, 
            User.password == password,
            User.user_type_number == 1
        ).first()

        if user:
            session['user_ID'] = user.user_ID
            return redirect(url_for('index'))
        else:
            return u'error'
        
    return render_template('login.html')