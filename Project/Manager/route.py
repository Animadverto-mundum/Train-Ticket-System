from flask import redirect, render_template, request, flash, url_for
from . import manager_bp
from .manager_auth import login_required
from model import db, Line


@manager_bp.route('/route_view')
@login_required
def route_view():
    '''查看所有线路'''
    routes = Line.query.filter().all()
    return render_template('manage_route_table.html', routes=routes)


@manager_bp.route('/route_edit')
@login_required
def route_edit():
    return render_template('manage_route_form.html')


@manager_bp.route('route_add', methods=['POST', 'GET'])
@login_required
def route_add():
    '''增加新的线路'''
    error = None
    if request.method == 'POST':
        # 获取表单数据
        route_name = request.form['route_name']
        departure_station = request.form['departure']
        arrival_station = request.form['arrival']
        line_distance = request.form['distance']
        # 处理错误
        if departure_station != arrival_station:
            error = 'station inconsistent'
        elif Line.query.filter(Line.line_name==route_name).first() is not None:
            error = f'line name {route_name} already exist.'
        # 没有错误，对数据库进行更新
        if error is None:
            new_line = Line(line_name=route_name, departure_station=departure_station, arrival_station=arrival_station,
                            line_distance=line_distance)
            db.session.add(new_line)
            db.session.commit()
            return redirect(url_for('manager_bp.route_view'))
        flash(error)

    return render_template('manage_route_form.html', routes=None)


@manager_bp.route('route_delete', methods=["GET"])
@login_required
def route_delete():
    '''删除一条线路'''
    route_id = request.args.get('id')
    route = Line.query.filter(Line.line_ID == route_id).first()  # 查找当前删除的普通用户

    db.session.delete(route)
    db.session.commit()

    return redirect(url_for('manager_bp.route_view'))