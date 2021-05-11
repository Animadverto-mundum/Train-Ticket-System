from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
from Manager.manager import manage_bp
from dataAnalysis.InitData import db_app
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()

# init blueprint
app.register_blueprint(manage_bp)
app.register_blueprint(db_app)
# app.add_url_rule('/', endpoint='manage_index')
# app.add_url_rule('/', endpoint='analysis')


# route
@app.route('/hello')
def hello():
    return 'Hello flask!'


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


if __name__ == '__main__':
    app.run(debug=True)
