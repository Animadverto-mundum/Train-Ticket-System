from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
from dataAnalysis.InitData import db_app
from User.User import user_bp
from dataAnalysis.Analysis import analysis_bp
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()

# 设置显示中文
app.config['JSON_AS_ASCII'] = False

# init blueprint
app.register_blueprint(db_app)
app.register_blueprint(user_bp)
app.register_blueprint(analysis_bp)
app.add_url_rule('/', endpoint='manage_login')
app.add_url_rule('/', endpoint='analysis')


# route
@app.route('/hello')
def hello():
    return 'Hello flask!'


@app.route('/manage_index')
def manage_index():
    return render_template('manage_index.html')


@app.route('/manage_login')
def manage_login():
    return render_template('user_login_register.html')


@app.route('/manage_route_form')
def manage_route_form():
    return render_template('manage_route_form.html')


@app.route('/manage_route_table')
def manage_route_table():
    return render_template('manage_route_table.html')


@app.route('/manage_station_form')
def manage_station_form():
    return render_template('manage_station_form.html')


@app.route('/manage_station_table')
def manage_station_table():
    return render_template('manage_station_table.html')


@app.route('/manage_ticket_form')
def manage_ticket_form():
    return render_template('manage_ticket_form.html')


@app.route('/manage_ticket_table')
def manage_ticket_table():
    return render_template('manage_ticket_table.html')


@app.route('/manage_train_form')
def manage_train_form():
    return render_template('manage_train_form.html')


@app.route('/manage_train_table')
def manage_train_table():
    return render_template('manage_train_table.html')


@app.route('/manage_user_form')
def manage_user_form():
    return render_template('manage_user_form.html')


@app.route('/manage_user_table')
def manage_user_table():
    return render_template('manage_user_table.html')

### 用户
@app.route('/user_index')
def user_index():
    return render_template('user_index.html')

@app.route('/user_register')
def user_register():
    return render_template('user_register.html')

@app.route('/user_login')
def user_login():
    return render_template('user_login.html')

@app.route('/user_checkTicket')
def user_checkTicket():
    return render_template('user_checkTicket.html')

@app.route('/user_buyTicket')
def user_buyTicket():
    return render_template('user_buyTicket.html')

@app.route('/user_refundTicket')
def user_refundTicket():
    return render_template('user_refundTicket.html')

###

if __name__ == '__main__':
    app.run(debug=True)
