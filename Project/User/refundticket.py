from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from . import user_bp
from .user_auth import login_required
import time


@user_bp.route('/checkrefundTicket', methods=['GET', 'POST'])
@login_required
def user_checkrefundticket():
    user_id = g.user.user_ID;
    localtime = time.localtime()
    current_time = time.strftime("%H:%M:%S", localtime)

    # Ʊ�� ���� ��·�� ����վ ����վ ����ʱ�� ����ʱ�� ��λ���� Ʊ�� ��λ��
    # ǰ��Ҫ�����û����͡���λ������ʾƱ��
    checkrefundtickets = db.session.query(TicketsSold.tickets_sold_ID, TrainNumber.train_number_ID,
                                          Line.line_name, Line.departure_station, Line.arrival_station,
                                          TrainNumber.departure_time, TrainNumber.arrival_time,
                                          FareInformation.seat_type, FareInformation.money,
                                          TicketsSold.seat).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID, FareInformation.fare_ID == TicketsSold.fare_ID,
               User.user_ID == user_id, TrainNumber.departure_time > current_time).all()

    return render_template('user_refundTicket.html', checkrefundtickets=checkrefundtickets)


@user_bp.route('refundtickt', methods=['GET', 'POST'])
@login_required
def user_refundticket():
    # ���������Ʊ��
    ticketsold_id = request.args.get('ticketsold_id')

    db.session.query.filter(TicketsSold.tickets_sold_ID == ticketsold_id).delete()
    db.session.commit()

    return redirect(url_for('user_bp.user_checkrefundticket'))
