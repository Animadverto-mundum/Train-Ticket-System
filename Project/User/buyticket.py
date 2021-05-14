from flask import request, redirect, render_template, url_for, flash
from model import *
from . import user_bp
from .user_auth import login_required


@user_bp.route('/user_inputbuyTicket', methods=['GET', 'POST'])
@login_required
def user_inputbuyticket():
    if request.method == 'POST':
        if request.form['submit'] == 'user_inputbuyticket':
            buy_arrival_station = request.form['arrival_station']
            buy_departure_station = request.form['departure_station']
            buy_departure_time = request.form['departure_time']
            buy_seat_type = request.form['seat_type']
            buy_error = None
            # buy_user_ID = db.session.query(User.user_ID).filter(User.user_name == global_username).first()

            if buy_arrival_station is None:
                buy_error = 'arrival station is required.'
            elif buy_departure_station is None:
                buy_error = 'departure station is required.'
            elif buy_departure_time is None:
                buy_error = 'departure time is required.'
            elif buy_seat_type is None:
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
                           TrainNumber.departure_time == buy_departure_time).all()
                return render_template('user_checkbuyTicket.html', checkbuytickets=checkbuytickets)

            flash(buy_error, 'query ticket')

    return render_template('user_buyTicket.html')


# 购票 插入数据 已购票信息
@user_bp.route('user_buyticket', methods=['GET', 'POST'])
@login_required
def user_buyticket():
    user_id = request.args.get('user_id')
    fare_id = request.args.get('fare_id')

    new_ticketsold = TicketsSold(fare_ID=fare_id, user_ID=user_id)
    db.session.add(new_ticketsold)
    db.session.commit()
    return redirect(url_for('user_inputbuyticket'))
