from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from . import user_bp


@user_bp.route('/user_checkTicket')
def user_checkticket():
    checktickets = db.session.query(TrainNumber.train_number_ID, Line.line_name,
                                    Line.departure_station, Line.arrival_station,
                                    TrainNumber.departure_time,TrainNumber.arrival_time,
                                    FareInformation.money).\
        filter(TrainNumber.train_number_ID == FareInformation.train_number_id,
               TrainNumber.line_ID == Line.line_ID).all()
    return render_template('user_checkTicket.html', checktickets=checktickets)


