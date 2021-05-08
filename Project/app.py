from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
from Auth.Auth import auth_app
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()

# init blueprint
app.register_blueprint(auth_app)

app.add_url_rule('/', endpoint='auth_app.register')

# route
@app.route('/hello')
def hello():
    return 'Hello flask!'

if __name__ == '__main__':
    app.run(debug=True)