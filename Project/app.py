from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db, User
from dataAnalysis.InitData import db_app
from User import user_bp
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
# app.add_url_rule('/', endpoint='manage_login')
# app.add_url_rule('/', endpoint='analysis')



if __name__ == '__main__':
    app.run(debug=True)
