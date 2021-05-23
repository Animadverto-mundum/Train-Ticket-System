import datetime
import time
import random
from flask import request, redirect, render_template, url_for, flash
# from model import *
from . import user_bp
from .user_auth import login_required
from model import db, FareInformation, TrainNumber, Line, Site, TicketsSold
from . import access_check
import os


@user_bp.route('/inputbuyTicket', methods=['GET', 'POST'])
@access_check(request)
def user_inputbuyticket():
    site_list = db.session.query(Site).filter().all()
    render_args = {'form_data': {},
                   'site_list': site_list,
                   'user_name': request.cookies.get('customer_name'),
                   'image_path': 'static/image/' + request.cookies.get('customer_name') + '.jpg',
                   'user_id': int(request.cookies.get('customer_id'))
                   }
    if request.method == 'POST':
        if request.form['submit'] == 'user_inputbuyticket':
            buy_arrival_station = request.form['arrival_station']
            buy_departure_station = request.form['departure_station']
            temp = request.form['departure_time']
            buy_departure_time = datetime.datetime.strptime(temp, "%H:%M:%S")
            seat_type = request.form['seat_type']
            if seat_type == "一等座":
                buy_seat_type = 1
            elif seat_type == "二等座":
                buy_seat_type = 2
            buy_error = None
            # buy_user_ID = db.session.query(User.user_ID).filter(User.user_name == global_username).first()=
            if buy_arrival_station == '':
                buy_error = 'arrival station is required.'
            elif buy_departure_station == '':
                buy_error = 'departure station is required.'
            elif buy_departure_time == '':
                buy_error = 'departure time is required.'
            elif buy_seat_type == '':
                buy_error = 'seat type is required.'
            # 票号、车次、线路号、座位类型、出发站、到达站、出发时间、到达时间
            # 用户ID、用户名、票价号
            if buy_error is None:
                checkbuytickets = db.session.query(FareInformation.fare_ID, TrainNumber.train_number_ID,
                                                   Line.line_ID, FareInformation.seat_type,
                                                   Line.departure_station, Line.arrival_station,
                                                   TrainNumber.departure_time, TrainNumber.arrival_time). \
                    filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
                           TrainNumber.line_ID == Line.line_ID,
                           Line.departure_station == buy_departure_station,
                           Line.arrival_station == buy_arrival_station,
                           FareInformation.seat_type == buy_seat_type,
                           TrainNumber.departure_time >= buy_departure_time).all()
                site_list = db.session.query(Site).filter().all()
                render_args = {'form_data': {},
                               'site_list': site_list,
                               'user_name': request.cookies.get('customer_name'),
                               'image_path': 'static/image/' + request.cookies.get('customer_name') + '.jpg',
                               'checkbuytickets': checkbuytickets,
                               'user_id': int(request.cookies.get('customer_id'))
                               }
                return render_template('user_checkbuyTicket.html', **render_args, vall=str(time.time()))
        flash(buy_error, 'query ticket')
    return render_template('user_buyTicket.html', **render_args, vall=str(time.time()))


# 购票 插入数据 已购票信息
@user_bp.route('buyticket', methods=['GET', 'POST'])
@access_check(request)
def user_buyticket():
    # 传入参数：用户ID、用户名、票价号
    user_id = int(request.cookies.get('customer_id'))
    user_name = request.cookies.get('customer_name')
    fare_id = request.args['fare_id']
    localtime = time.localtime()
    temp = time.strftime("%Y-%m-%d", localtime)
    current_date = datetime.datetime.strptime(temp, '%Y-%m-%d').date()

    while True:
        seat = random.randint(1, 1000)
        if len(db.session.query(TicketsSold).filter(TicketsSold.fare_ID == fare_id) \
                       .filter(TicketsSold.seat == seat).all()):
            continue
        break

    new_ticketsold = TicketsSold(fare_ID=fare_id, user_ID=user_id, seat=seat, departure_date=current_date)
    db.session.add(new_ticketsold)
    db.session.commit()
    return redirect(url_for('user_bp.user_inputbuyticket'))
