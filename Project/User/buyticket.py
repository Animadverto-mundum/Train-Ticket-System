import datetime
import time
from random import random
from flask import request, redirect, render_template, url_for, flash
# from model import *
from . import user_bp
from .user_auth import login_required
from model import *


@user_bp.route('/inputbuyTicket', methods=['GET', 'POST'])
def user_inputbuyticket():
    if request.method == 'POST':
        if request.form['submit'] == 'user_inputbuyticket':
            buy_arrival_station = request.form['arrival_station']
            buy_departure_station = request.form['departure_station']
            temp = request.form['departure_time']
            buy_departure_time = datetime.datetime.strptime(temp, "%H:%M:%S")
            buy_seat_type = request.form['seat_type']
            buy_error = None
            # buy_user_ID = db.session.query(User.user_ID).filter(User.user_name == global_username).first()

            if buy_arrival_station == '':
                buy_error = 'arrival station is required.'
            elif buy_departure_station == '':
                buy_error = 'departure station is required.'
            elif buy_departure_time == '':
                buy_error = 'departure time is required.'
            elif buy_seat_type == '':
                buy_error = 'seat type is required.'

            if buy_error is None:
                checkbuytickets = db.session.query(TrainNumber.train_number_ID, Line.line_ID,
                                                   FareInformation.seat_type,
                                                   Line.departure_station, Line.arrival_station,
                                                   TrainNumber.departure_time,
                                                   TrainNumber.arrival_time). \
                    filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
                           TrainNumber.line_ID == Line.line_ID,
                           Line.departure_station == buy_departure_station,
                           Line.arrival_station == buy_arrival_station,
                           FareInformation.seat_type == buy_seat_type,
                           TrainNumber.departure_time >= buy_departure_time).all()

                # print(buy_departure_time)
                # temp = datetime.datetime.strptime(buy_departure_time, "%H:%M:%S")
                # print(temp)
                # temp1 = "00:00:00"
                # temp2 = datetime.datetime.strptime(temp1, "%H:%M:%S")
                # if temp == temp2:
                #     print("结果相同")
                # else:
                #     print("结果不同")
                return render_template('user_checkbuyTicket.html', checkbuytickets=checkbuytickets)

        flash(buy_error, 'query ticket')

    return render_template('user_buyTicket1.html')


# 购票 插入数据 已购票信息
@user_bp.route('buyticket', methods=['GET', 'POST'])
@login_required
def user_buyticket():
    user_id = request.args.get('user_id')
    fare_id = request.args.get('fare_id')
    localtime = time.localtime()
    current_date = time.strftime("%Y-%m-%d", localtime)

    while True:
        seat = random.randint(1, 1000)
        if len(db.session.query(TicketsSold).filter(TicketsSold.fare_ID == fare_info.fare_ID).\
                       filter(TicketsSold.seat == seat).all()):
            continue
        break

    new_ticketsold = TicketsSold(fare_ID=fare_id, user_ID=user_id, seat=seat, departure_date=current_date)
    db.session.add(new_ticketsold)
    db.session.commit()
    return redirect(url_for('user_bp.user_inputbuyticket'))
