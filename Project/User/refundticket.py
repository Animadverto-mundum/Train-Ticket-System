import datetime

from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from . import user_bp
from .user_auth import login_required
import time


@user_bp.route('/checkrefundTicket', methods=['GET', 'POST'])
# @login_required
def user_checkrefundticket():
    # user_id = g.user.user_ID;
    localtime = time.localtime()
    current_time = time.strftime("%H:%M:%S", localtime)

    s = datetime.datetime.strptime("00:00:00", '%H:%M:%S').time()

    # 票号 车次 线路名 出发站 到达站 出发时间 到达时间 座位类型 票价 座位号
    # 前端要根据用户类型、座位类型显示票价
    checkrefundtickets = db.session.query(TicketsSold.tickets_sold_ID, TrainNumber.train_number_ID,
                                          Line.line_name, Line.departure_station, Line.arrival_station,
                                          TrainNumber.departure_time, TrainNumber.arrival_time,
                                          FareInformation.seat_type, FareInformation.money,
                                          TicketsSold.seat).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID, FareInformation.fare_ID == TicketsSold.fare_ID,
               TicketsSold.user_ID == 1, TrainNumber.departure_time > s).all()

    return render_template('user_refundTicket.html', checkrefundtickets=checkrefundtickets)


@user_bp.route('refundtickt', methods=['GET', 'POST'])
# @login_required
def user_refundticket():
    # 传入参数：票号
    ticketsold_id = request.args['ticketsold_id']

    delete_item = db.session.query(TicketsSold).filter(TicketsSold.tickets_sold_ID == ticketsold_id).first()
    db.session.delete(delete_item)
    db.session.commit()

    return redirect(url_for('user_bp.user_checkrefundticket'))
