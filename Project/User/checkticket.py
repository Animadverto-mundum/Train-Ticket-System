from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import db, TrainNumber, FareInformation, Line
from . import user_bp
import os
import time

@user_bp.route('/user_checkTicket')
def user_checkticket():
    user_name = request.cookies.get('customer_name')
    checktickets = db.session.query(TrainNumber.train_number_ID, Line.line_name,
                                    Line.departure_station, Line.arrival_station,
                                    TrainNumber.departure_time,TrainNumber.arrival_time,
                                    FareInformation.money).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID).all()
    render_args={
        'user_name':user_name,
        'checktickets':checktickets,
        'image_path':'static/image/' + user_name + '.jpg'
    }
    return render_template('user_checkTicket.html', **render_args, vall=str(time.time()))


