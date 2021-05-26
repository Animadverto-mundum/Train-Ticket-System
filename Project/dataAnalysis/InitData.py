import pandas
from sqlalchemy import event

from model import *
from flask import Blueprint
from DataAnalysis.Analysis_way import *
import datetime
db_app = Blueprint('db_app', __name__, static_folder='static', template_folder='templates', url_prefix='/db')


# # 从数据库提取数据+存入数据库
@event.listens_for(TicketsSold, 'after_insert')
def modify_raw_data():
    sold=TicketsSold.query(TicketsSold.fare_ID).filter().order_by(TicketsSold.tickets_sold_ID.desc()).first()
    train_id=FareInformation.query(FareInformation.train_number_id,FareInformation.departure_time).filter(FareInformation.fare_ID==sold.fare_ID).first()

    data_updata=TrainNumber.query(TrainNumber.train_ID,TrainNumber.departure_time,TrainNumber.train_number_ID,TrainNumber.first_tickets_remain_num,TrainNumber.second_tickets_remain_num)\
        .filter(TrainNumber.train_number_ID==train_id.train_number_ID,TrainNumber.departure_time==train_id.departure_time).all()

    train_type=Train.query(Train.type_number).filter(data_updata.train_ID==Train.train_ID).first()

    seats=Vehicles.query(Vehicles.first_class_seats,Vehicles.second_class_seats).filter(train_type.type_number==Train.type_number).first()

    time_list = []
    value_list = []
    train_list = []
    for data in data_updata:
        time_list.append(data.departure_time)
        train_list.append(data.train_number_ID)
        value=seats.first_class_seats+seats.second_class_seats-(data.first_tickets_remain_num+data.second_tickets_remain_num)
        value_list.append(value)
    preview_list = {'时间': time_list, '数值': value_list,'车次':train_list}

    for p in preview_list:
        predict_data = PredictData(time=p['时间'], train_number_ID=p['车次'], value=p['数值'])
        db.session.add(predict_data)
    db.session.commit()


# 数据测试
@db_app.route('/test')
def testData():
    test_data = RawData(time='2020-05-21 23:51:00', value=10, train_number_ID=72)
    db.session.add(test_data)
    db.session.commit()
    return "test"


# 数据预测测试
@db_app.route('/InitPredict')
def initPredict():
    sensor = 'A1'
    periods = 50
    freq = "1D"
    data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
    time_list = []
    value_list = []
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    preview_list = dataPreview(data_df[['时间', '数值']], periods=periods, freq=freq)
    for p in preview_list:
        print(p)
        predict_data = PredictData(time=p['时间'], yhat=p['yhat'], yhat_lower=p['yhat_lower'],
                                   yhat_upper=p['yhat_upper'], train_number_ID=sensor)
        db.session.add(predict_data)
    db.session.commit()
    return "预测数据初始化完毕"


@db_app.route('/InitData')
def InitData():
    print("进来了")
    df = pandas.read_csv('D:\code_work\Train-Ticket-System-new\Project\DataAnalysis\数据.csv')
    print(df)
    for sensor_name in list(df)[1:]:
        id = 'D521'
        for index, row in df.iterrows():
            time = row['Time']
            value = row[sensor_name]
            new_data = RawData(time=time, value=value, train_number_ID=id)
            db.session.add(new_data)
        db.session.commit()
    return "数据初始化成功"


@db_app.route('/Trend')
def Trend():
    print("进来了")
    sensor = 'A1'
    periods = '2H'
    data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
    time_list = []
    value_list = []
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    preview_list = dataTrend(data_df[['时间', '数值']])
    # print(preview_list)
