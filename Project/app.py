from flask import Flask, request, json, Response, redirect, url_for, session, render_template
from model import db
from Manager import manager_bp
from User import user_bp
import config


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)  # 配置文件
    db.init_app(app)

    # init blueprint
    app.register_blueprint(manager_bp)
    app.register_blueprint(user_bp)

    return app


app = create_app()


# route
@app.route('/')
def hello():
    return redirect(url_for('user_bp.user_index'))

if __name__ == '__main__':
    app.run(debug=True, port=8088)
