from flask import render_template, redirect, url_for, session, request,flash
from . import manager_bp, access_check
import random
from model import *
import datetime
from sqlalchemy import func
from DataAnalysis.Analysis_way import *


@manager_bp.route('/index', methods=['GET', 'POST'])
def manager_index():
    if not access_check(request, 0):
        response = redirect(url_for('manager_bp.manager_auth'))
        response.delete_cookie('user_name')
        response.delete_cookie('user_type')
        return response
    user_name = request.cookies.get('user_name')

    # 在index界面上添加数据分析+预测部分
    # 功能1：默认显示今日总客流量
    today = datetime.date.today()
    ticket_sold_today = db.session.query(func.count(TicketsSold.tickets_sold_ID)).filter(TicketsSold.departure_date==today).scalar()

    # 其余功能
    if request.method == 'POST':
        print(request.values,"请求的值")
        # 功能2:查询特定日期特定车次的乘车人数
        errno = None
        if request.form.get('type') == 'select':
            data = request.form.get('data')
            train_id = request.form.get('train_num')
            ticket_sold = db.session.query(func.count(TicketsSold.tickets_sold_ID)).filter(TicketsSold.departure_date == data,
                                                                                           FareInformation.train_number_id==train_id,
                                                                                           TicketsSold.fare_ID==FareInformation.fare_ID).scalar()
            return render_template('manage_index.html',ticket_sold=ticket_sold)

        # 功能3：预测数据
        if request.form.get('type')=='数据预测':
            print('进来预测')
            periods = int(request.form['periods'])
            freq = request.form['freq']
            sensor = request.form['train_number_ID']
            data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
            data_df=createdataframe(data_list)
            print("预测姐u但",periods)
            predict_list,pic = dataPreview(data_df[['时间', '数值']], periods=periods, freq=freq)
            # plt.show()
            plt.savefig('./temp.png', format='png')
            img_stream=tran_pic('./temp.png')
            print("返回去",predict_list)
            render_args = {
                'predict_list': predict_list,
                'pic': img_stream,
                'user_name':user_name,
                'ticket_sold_today':ticket_sold_today

            }
            return render_template("manage_index.html",**render_args)

        # 功能4：分析趋势
        elif request.form['type']=='数据趋势分析':
            sensor = request.form['train_number_ID']
            begin_time = datetime.datetime.strptime(request.form['begin_time'],"%Y%m%d")
            end_time = datetime.datetime.strptime(request.form['end_time'],"%Y%m%d")
            print(sensor,end_time,begin_time,"进来了吗")
            error = None
            if begin_time>datetime.datetime.now() or end_time>datetime.datetime.now():
                error = "输入时间不可以早于当前时间!"
            elif begin_time>end_time:
                error = "开始时间必须早于结束时间!"
            if error is None:
                data_list = RawData.query.filter((RawData.train_number_ID == sensor) & (begin_time <= RawData.time) & (
                            RawData.time <= end_time)).order_by(RawData.time.desc()).all()
                data_df = createdataframe(data_list)
                if data_df.empty:
                    error = "该时间段内没有数据!"
                else:
                    describe_list = data_df.describe().to_dict()
                    trend_list,pic = dataTrend(data_df[['时间', '数值']])
                    plt.savefig('./temp2.png', format='png')
                    img_stream = tran_pic('./temp2.png')
                    render_args = {
                        'trend_list':trend_list,
                        'pic_trend': img_stream,
                        'describe_list': describe_list,
                    }
                    return render_template("manage_index.html",**render_args)
        # 反馈输入错误
        if error:
            print("错误是",error)
        if error is not None:
            flash(error,'trend')


    return render_template('manage_index.html', user_name=user_name,ticket_sold_today=ticket_sold_today)


@manager_bp.route('/logout')
def manager_logout():
    session.clear()
    response = redirect(url_for('manager_bp.manager_auth'))
    response.delete_cookie("user_name")
    response.delete_cookie("user_type")
    return response
