from flask_sqlalchemy import SQLAlchemy
from DataAnalysis import *

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
    train_number_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    train_ID = db.Column(db.Integer, db.ForeignKey('train.train_ID', ondelete='CASCADE'), nullable=False)
    line_ID = db.Column(db.Integer, db.ForeignKey('line.line_ID', ondelete='CASCADE'), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)


class FareInformation(db.Model):  # 票价信息
    __tablename__ = 'fare_information'
    fare_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    train_number_id = db.Column(db.Integer, db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
                                nullable=False)
    seat_type = db.Column(db.Integer, nullable=False)
    money = db.Column(db.Integer, nullable=False)


class TicketsSold(db.Model):
    __tablename__ = 'tickets_sold'
    tickets_sold_ID = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    fare_ID = db.Column(db.Integer, db.ForeignKey('fare_information.fare_ID', ondelete='CASCADE'), nullable=False)
    user_ID = db.Column(db.Integer, db.ForeignKey('user.user_ID', ondelete='CASCADE'), nullable=False)
    seat = db.Column(db.Integer, nullable=False)


# 拓展功能用数据库
# 原始数据（具体到为一车次的在某个时间的人数）
class RawData(db.Model):
    __tablename__ = 'raw_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True)
    train_number_ID = db.Column(db.Integer, db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
                                nullable=False)
    value = db.Column(db.Integer, nullable=False)


# 预测数据表
class PredictData(db.Model):
    __tablename__ = 'predict_data'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    time = db.Column(db.DateTime, nullable=True)
    train_number_ID = db.Column(db.Integer, db.ForeignKey('train_number.train_number_ID', ondelete='CASCADE'),
                                nullable=False)
    yhat = db.Column(db.Float, nullable=False)
    yhat_lower = db.Column(db.Float, nullable=True)
    yhat_upper = db.Column(db.Float, nullable=True)


# 从数据库提取数据+存入数据库
@event.listens_for(RawData, 'after_insert')
def preProcessData(mapper, connection, target, periods):
    data_list = RawData.query.filter(RawData.train_number_ID == target).order_by(RawData.time.desc()).all()
    time_list = []
    value_list = []
    sensor = data_list[0].train_number_ID
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    preview_list = dataPreview(data_df[['时间', '数值']], periods)

    for p in preview_list:
        predict_data = PredictData(time=p['时间'], yhat=p['yhat'], yhat_lower=p['yhat_lower'],
                                   yhat_upper=p['yhat_upper'], train_number_ID=sensor)
        db.session.add(predict_data)
    db.session.commit()


# 数据测试
@db_bp.route('/test')
def testData():
    test_data = RawData(time='2020-05-21 23:55:00', value=4999.99, train_number_ID=72)
    db.session.add(test_data)
    db.session.commit()
    return "test"

# 数据预测测试
@db_bp.route('/InitPredict')
def initPredict():
    sensor = 1
    periods = '5min'

    data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
    time_list = []
    value_list = []
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    preview_list = dataPreview(data_df[['时间', '数值']], periods)
    for p in preview_list:
        predict_data = PredictData(time=p['时间'], yhat=p['yhat'], yhat_lower=p['yhat_lower'],
                                   yhat_upper=p['yhat_upper'], train_number_ID=sensor)
        db.session.add(predict_data)
    db.session.commit()
    return "预测数据初始化完毕"
