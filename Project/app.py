from flask import Flask, request, json, Response
from flask_sqlalchemy import SQLAlchemy
from exts import db
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    return app


app = create_app()

# 此处为路由表
@app.route('/')
def index():
    return 'Hello flask!'


if __name__ == '__main__':
    app.run(debug=True)