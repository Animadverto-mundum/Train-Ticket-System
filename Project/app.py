from flask import Flask, redirect, url_for, render_template
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


@app.errorhandler(404)
def page_not_found(e):
    render_args = {
        'error_code': '404',
        'error_message': '看来好像找不到你要的东西'
    }
    return render_template("error_page.html", **render_args)

@app.errorhandler(500)
def page_not_found(e):
    render_args = {
        'error_code': '500',
        'error_message': '写的参数是不是有错呢？'
    }
    return render_template("error_page.html", **render_args)
# route
@app.route('/')
def hello():
    return redirect(url_for('user_bp.user_index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
