from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
from Login.Login import login_app
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()
app.register_blueprint(login_app)

# 此处为路由表



if __name__ == '__main__':
    app.run(debug=True)