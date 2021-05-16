import matplotlib.pyplot as plt
from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *
from flask import jsonify
import datetime
from DataAnalysis.Analysis_way import *
import base64
from PIL import Image
from io import BytesIO

analysis_bp = Blueprint('analysis_bp', __name__, static_folder='static', template_folder='templates',
                        url_prefix='/analysis')


@analysis_bp.route('/predict', methods=['GET', 'POST'])
def Predict():
    if request.method == 'POST':
        if request.form['type']=='predict':
            periods = int(request.form['periods'])
            freq = request.form['freq']
            sensor = request.form['train_number_ID']
            data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
            data_df=createdataframe(data_list)
            predict_list,pic = dataPreview(data_df[['时间', '数值']], periods=periods, freq=freq)
            plt.savefig('./temp.png', format='png')
            img_stream=tran_pic('./temp.png')
            render_args = {
                'predict_list': predict_list,
                'pic': img_stream,
            }
            return render_template("manger_predict.html",**render_args)

        elif request.form['type']=='trend' or request.form['type']=='describe':
            sensor = request.form['train_number_ID']
            begin_time = datetime.datetime.strptime(request.form['begin_time'],"%Y%m%d")
            end_time = datetime.datetime.strptime(request.form['end_time'],"%Y%m%d")
            print(sensor,end_time,begin_time)
            error = None
            if begin_time>datetime.datetime.now() or end_time>datetime.datetime.now():
                error = "The input time cannot be later than the current time!"
            elif begin_time>end_time:
                error = "The start time must be earlier than the end time!"
            if error is None:
                data_list = RawData.query.filter((RawData.train_number_ID == sensor) & (begin_time <= RawData.time) & (
                            RawData.time <= end_time)).order_by(RawData.time.desc()).all()
                data_df = createdataframe(data_list)
                if data_df.empty:
                    error = "There is no data in the database for this train during this time period!"
                elif request.form['type']=='trend':
                    trend_list,pic = dataTrend(data_df[['时间', '数值']])
                    plt.savefig('./temp2.png', format='png')
                    img_stream = tran_pic('./temp2.png')
                    render_args = {
                        'trend_list':trend_list,
                        'pic': img_stream,
                    }
                    return render_template("manger_predict.html",**render_args)

                elif request.form['type']=='describe':
                    describe_list=data_df.describe().to_dict()
                    print(describe_list)
                    render_args = {
                        'describe_list': describe_list,

                    }
                    return render_template("manger_predict.html",**render_args)

            if error is not None:
                flash(error,'trend')


    return render_template('manger_predict.html')


def createdataframe(data_list):
    time_list = []
    value_list = []
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    return data_df

def tran_pic(path):
    with open(path, 'rb') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream).decode()
        return img_stream