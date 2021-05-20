from flask import redirect, render_template, url_for, request
from . import manager_bp, access_check
from model import db, Site
import random

@manager_bp.route('/station_view')
def station_view():
    '''查看所有的的站点'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    stations = db.session.query(Site.site_name, Site.site_capacity_level).filter().all()
    user_name = request.cookies.get('user_name')
    return render_template('manage_station_table.html', stations=stations, user_name=user_name)

@manager_bp.route('/station_add', methods=["GET", "POST"])
def station_add():
    '''添加单个的车站'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    error = None
    if request.method == 'POST':
        new_name = request.form['station_name']
        level = eval(request.form.get('capacity_level'))
        # 处理错误
        if Site.query.filter(Site.site_name==new_name).first() is not None:
            error = 'Site {} already exist'.format(new_name)
        # 没有错误
        if error is None:
            new_station = Site(site_name=new_name, site_capacity_level=level, opening_time='00:00:00', closing_time='23:59:59')
            db.session.add(new_station)
            db.session.commit()
            # 跳转到查看页
            return redirect(url_for('manager_bp.station_view'))
    user_name = request.cookies.get('user_name')
    return render_template('manage_station_form.html', type='add', station=None, user_name=user_name)
    

@manager_bp.route('/station_edit', methods=["GET", "POST"])
def station_edit():
    '''编辑单个的车站等级'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    site_name = request.args.get('station_name')
    station = Site.query.filter(Site.site_name==site_name).first() # 查找当前删除的普通用户    
    if request.method == 'POST':
        level = eval(request.form.get('capacity_level'))
        new_station = Site.query.filter(Site.site_name==site_name).update({
            "site_capacity_level":level})
        db.session.commit()
        return redirect(url_for('manager_bp.station_view'))
    
    user_name = request.cookies.get('user_name')
    return render_template('manage_station_form.html', type='edit', station=station, user_name=user_name)

@manager_bp.route('/station_delete', methods=["GET"])
def station_delete():
    '''删除单个车站'''
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    site_name = request.args.get('station_name')
    station = Site.query.filter(Site.site_name==site_name).first() # 查找当前删除的普通用户

    db.session.delete(station)
    db.session.commit()

    user_name = request.cookies.get('user_name')
    return redirect(url_for('manager_bp.station_view'))