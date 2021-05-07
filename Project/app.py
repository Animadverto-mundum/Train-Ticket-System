from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()

# 此处为路由表
@app.route('/hello')
def index():
    return 'Hello flask!'

@app.route('/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User(user_name=username, password=password, user_type_number=1)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
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


if __name__ == '__main__':
    app.run(debug=True)