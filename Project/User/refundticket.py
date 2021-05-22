import datetime
from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from . import user_bp
from .user_auth import login_required
import time


@user_bp.route('/checkrefundTicket', methods=['GET', 'POST'])
# @login_required
def user_checkrefundticket():
    user_id = int(request.cookies.get('customer_id'))
    localtime = time.localtime()
    current_time = time.strftime("%H:%M:%S", localtime)
    current_user = db.session.query(User).filter(User.user_ID==user_id).first()

    # ����ʹ�� �鿴��������Ʊ
    s = datetime.datetime.strptime("00:00:00", '%H:%M:%S').time()

    # Ʊ�� ���� ��·�� ����վ ����վ ����ʱ�� ����ʱ�� ��λ���� Ʊ�� ��λ��
    # ǰ�˸����û�������ʾƱ��
    checkrefundtickets = db.session.query(TicketsSold.tickets_sold_ID, TrainNumber.train_number_ID,
                                          Line.line_name, Line.departure_station, Line.arrival_station,
                                          TrainNumber.departure_time, TrainNumber.arrival_time,
                                          FareInformation.seat_type, FareInformation.money,
                                          TicketsSold.seat).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID, FareInformation.fare_ID == TicketsSold.fare_ID,
               TicketsSold.user_ID == user_id, TrainNumber.departure_time > s).all()


    render_args = {
        'checkrefundtickets': checkrefundtickets,
        'user_type': current_user.user_type_number,
        'user_id': int(request.cookies.get('customer_id')),
        'user_name': request.cookies.get('customer_name')
    }

    return render_template('user_refundTicket.html', **render_args)


@user_bp.route('refundtickt', methods=['GET', 'POST'])
# @login_required
def user_refundticket():
    # ���������Ʊ��
    ticketsold_id = request.args['ticketsold_id']

    delete_item = db.session.query(TicketsSold).filter(TicketsSold.tickets_sold_ID == ticketsold_id).first()
    db.session.delete(delete_item)
    db.session.commit()

    return redirect(url_for('user_bp.user_checkrefundticket'))
