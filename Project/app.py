from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
from model import db
# from dataAnalysis.InitData import db_app
import config

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)
    return app


app = create_app()

# init blueprint
from Manager import manager_bp
app.register_blueprint(manager_bp)

# app.register_blueprint(db_app)
# app.add_url_rule('/', endpoint='manage_index')
# app.add_url_rule('/', endpoint='analysis')


# route
@app.route('/hello')
def hello():
    return 'Hello flask!'


if __name__ == '__main__':
    app.run(debug=True,port=8080)
