from flask import redirect, render_template, request, redirect, url_for, flash
from . import manager_bp, access_check
from model import db, TrainNumber, Line, TicketsSold, FareInformation, User
import random


@manager_bp.route('/ticket_view', methods = ['GET'])
@access_check(request, '3')
def ticket_view():
    ret = db.session.query(TrainNumber, Line, TicketsSold, FareInformation, User)\
        .filter(TrainNumber.line_ID == Line.line_ID)\
        .filter(TicketsSold.fare_ID == FareInformation.fare_ID)\
        .filter(FareInformation.train_number_id == TrainNumber.train_number_ID)\
        .filter(TicketsSold.user_ID == User.user_ID).all()
    render_args = {
        'ret': ret, 
        'user_name': request.cookies.get('user_name'),
        }
    return render_template('manage_ticket_table.html', **render_args)


@manager_bp.route('/ticket_delete', methods = ['GET'])
@access_check(request, '3')
def ticket_delete():
    delete_tickets_sold_ID = request.args.get('delete_tickets_sold_ID')
    delete_item = db.session.query(TicketsSold).filter(TicketsSold.tickets_sold_ID == delete_tickets_sold_ID).first()
    db.session.delete(delete_item)
    db.session.commit()
    return redirect(url_for('manager_bp.ticket_view'))


@manager_bp.route('/ticket_edit')
@access_check(request, '3')
def ticket_edit():
    train_number_ID_list = db.session.query(TrainNumber, Line).filter(TrainNumber.line_ID == Line.line_ID).all()
    render_args = {'form_data': {}, 
        'train_number_ID_list': train_number_ID_list,
        'user_name': request.cookies.get('user_name')
        }
    return render_template('manage_ticket_form.html', **render_args)


@manager_bp.route('/ticket_add', methods = ['POST'])
@access_check(request, '3')
def ticket_add():
    if request.form.get("user_certificate_type") == 'user_name':
        user_operating = db.session.query(User)\
            .filter(User.user_name == request.form.get("user_certificate")).first()
    elif request.form.get("user_certificate_type") == 'user_id':
        user_operating = db.session.query(User)\
            .filter(User.user_ID == request.form.get("user_certificate")).first()
        
    if request.form.get("seat_type") == 'on':
        fare_info = db.session.query(FareInformation)\
            .filter(FareInformation.train_number_id == request.form.get("train_number_ID").split('-')[0])\
            .filter(FareInformation.seat_type == 1).first()
    else:
        fare_info = db.session.query(FareInformation)\
            .filter(FareInformation.train_number_id == request.form.get("train_number_ID").split('-')[0])\
            .filter(FareInformation.seat_type == 2).first()
    while True:
        seat = random.randint(1, 1000)
        if len(db.session.query(TicketsSold).filter(TicketsSold.fare_ID==fare_info.fare_ID)\
            .filter(TicketsSold.seat==seat).all()):
            continue
        break
    new_ticket = TicketsSold(fare_ID=fare_info.fare_ID, user_ID=user_operating.user_ID,\
         seat=seat, departure_date=request.form.get("train_departure_date"))
    db.session.add(new_ticket)
    db.session.commit()
    return redirect(url_for('manager_bp.ticket_view'))


@manager_bp.route('/ticket_query', methods = ['POST'])
@access_check(request, '3')
def ticket_query():
    if request.form.get("user_certificate_type") == 'user_name':
        user_operating = db.session.query(User)\
            .filter(User.user_name == request.form.get("user_certificate")).first()
    elif request.form.get("user_certificate_type") == 'user_id':
        user_operating = db.session.query(User)\
            .filter(User.user_ID == request.form.get("user_certificate")).first()
        
    fare_info = db.session.query(FareInformation)\
        .filter(FareInformation.train_number_id == request.form.get("train_number_ID").split('-')[0])\
        .filter(FareInformation.seat_type == int(request.form.get("seat_type"))).first()
    try:
        price = fare_info.money
        if user_operating.user_type_number == 2:
            price *= 0.8
        price = 'CNY: %d' % price
    except:
        price = "please complete form"
    flash(price)
    form_data = {
          "user_certificate_type": request.form.get("user_certificate_type"),
          "user_certificate": request.form.get("user_certificate"),
          "train_number_ID": request.form.get("train_number_ID"),
          "train_departure_date": request.form.get("train_departure_date"),
          "seat_type": request.form.get("seat_type")
        }
    if form_data['user_certificate_type'] == 'user_id':
        form_data['user_certificate_type'] = 'selected'
    if form_data['seat_type'] == '2':
        form_data['seat_type'] = 'selected'
    render_args = {'form_data': form_data,
            'user_name': request.cookies.get('user_name')
    }
    return render_template('manage_ticket_form.html', **render_args)