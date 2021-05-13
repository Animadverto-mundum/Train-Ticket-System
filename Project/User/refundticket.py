from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from . import user_bp
from .user_auth import login_required
import time


@user_bp.route('/user_checkrefundTicket', methods=['GET', 'POST'])
@login_required
def user_checkrefundticket():
    user_id = request.args.get('user_id')
    localtime = time.localtime()
    year = localtime.tm_year
    month = localtime.tm_mon
    day = localtime.tm_mday
    hour = localtime.tm_hour
    minute = localtime.tm_min
    sec = localtime.tm_sec

    # 格式化成2016-03-20 11:45:39形式
    time_format = time.strftime("%Y-%m-%d %H:%M:%S", localtime)

    checkrefundtickets = db.session.query(TrainNumber.train_number_ID, Line.line_name,
                                          Line.departure_station, Line.arrival_station,
                                          TrainNumber.departure_time, TrainNumber.arrival_time,
                                          FareInformation.seat_type, FareInformation.money,
                                          TicketsSold.seat).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID, FareInformation.fare_ID == TicketsSold.fare_ID,
               User.user_ID == user_id).all()

    return render_template('user_refundTicket.html', checkrefundtickets=checkrefundtickets,
                           time_format=time_format)


@user_bp.route('user_refundtickt', methods=['GET', 'POST'])
@login_required
def user_refundticket():
    ticketsold_id = request.args.get('ticketsold_id')

    db.session.query.filter(TicketsSold.tickets_sold_ID == ticketsold_id).delete()
    db.session.commit()

    return redirect(url_for('user_bp.user_checkrefundticket'))
