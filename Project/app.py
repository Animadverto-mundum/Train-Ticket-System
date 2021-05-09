from flask import Flask, request, json, Response, render_template
from flask_sqlalchemy import SQLAlchemy
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    return app


app = create_app()


# 此处为路由表
# @app.route('/')
# def index():
#     return 'Hello flask!'

@app.route("/")  # 首页
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True, port=8888)
