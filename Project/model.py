from flask_sqlalchemy import SQLAlchemy
# from dataAnalysis.Analysis_way import *

db = SQLAlchemy()


class UserStaff(db.Model):
    __tablename__ = 'staff'
    staff_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    department_type_number = db.Column(db.Integer, nullable=False)


class User(db.Model):
    __tablename__ = 'user'
    user_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type_number = db.Column(db.Integer, nullable=False)


class Site(db.Model):
    __tablename__ = 'site'
    site_name = db.Column(db.String(20), primary_key=True, nullable=False)
    site_capacity_level = db.Column(db.Integer, nullable=False)
    opening_time = db.Column(db.Time, nullable=False)
    closing_time = db.Column(db.Time, nullable=False)


class Line(db.Model):
    __tablename__ = 'line'
    line_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    line_name = db.Column(db.String(20), unique=True, nullable=False)
    departure_station = db.Column(db.String(20), db.ForeignKey('site.site_name', ondelete='CASCADE'), nullable=False)
    arrival_station = db.Column(db.String(20), db.ForeignKey('site.site_name', ondelete='CASCADE'), nullable=False)
    line_distance = db.Column(db.Integer, nullable=False)


class Train(db.Model):  # 具体车表
    __tablename__ = 'train'
    train_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    type_number = db.Column(db.Integer, db.ForeignKey('vehicles.type_number', ondelete='CASCADE'), nullable=False)


class Vehicles(db.Model):  # 车类型表
    __tablename__ = 'vehicles'
    type_number = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    first_class_seats = db.Column(db.Integer, nullable=False)
    second_class_seats = db.Column(db.Integer, nullable=False)


class TrainNumber(db.Model):  # 车次表
    __tablename__ = 'train_number'
    train_number_ID = db.Column(db.String(20), primary_key=True, nullable=False)
    train_ID = db.Column(db.Integer, db.ForeignKey('train.train_ID', ondelete='CASCADE'), nullable=False)
    line_ID = db.Column(db.Integer, db.ForeignKey('line.line_ID', ondelete='CASCADE'), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)


class FareInformation(db.Model):  # 票价信息
    __tablename__ = 'fare_information'
    fare_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    train_number_id = db.Column(db.String(20), db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
                                nullable=False)
    seat_type = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)


class TicketsSold(db.Model):
    __tablename__ = 'tickets_sold'
    tickets_sold_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fare_ID = db.Column(db.Integer, db.ForeignKey('fare_information.fare_ID', ondelete='CASCADE'), nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID', ondelete='CASCADE'), nullable=False)
    seat = db.Column(db.Integer, nullable=False)
    departure_date = db.Column(db.Date, nullable=False)


# 拓展功能用数据库
# 原始数据（具体到为一车次的在某个时间的人数）
class RawData(db.Model):
    __tablename__ = 'raw_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True)
    # train_number_ID = db.Column(db.Integer, db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
    #                             nullable=False)
    train_number_ID = db.Column(db.String(28), nullable=False)
    value = db.Column(db.Float, nullable=False)


# 预测数据表
class PredictData(db.Model):
    __tablename__ = 'predict_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True)
    # train_number_ID = db.Column(db.Integer, db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
    #                             nullable=False)
    train_number_ID = db.Column(db.String(28), nullable=False)
    yhat = db.Column(db.Float, nullable=False)
    yhat_lower = db.Column(db.Float, nullable=True)
    yhat_upper = db.Column(db.Float, nullable=True)
