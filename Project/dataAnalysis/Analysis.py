from flask import Blueprint, request, redirect, render_template, url_for, session, flash, g
from model import *

analysis_bp = Blueprint('analysis_bp', __name__, static_folder='static', template_folder='templates',
                        url_prefix='/analysis')


@analysis_bp.route('/predict', methods=['GET', 'POST'])
def Predict():
    # if request.method == 'POST':
    # periods = request.form['periods']
    # freq = request.form['freq']
    # sensor = request.form['train_number_ID']

    periods = 50
    freq = '2H'
    sensor = "A1"

    data_list = RawData.query.filter(RawData.train_number_ID == sensor).order_by(RawData.time.desc()).all()
    time_list = []
    value_list = []
    for data in data_list:
        time_list.append(data.time)
        value_list.append(data.value)
    data_dic = {'时间': time_list, '数值': value_list}
    data_df = pd.DataFrame(data=data_dic)  # 构造dataframe
    predict_list = dataPreview(data_df[['时间', '数值']], periods=periods, freq=freq)
    print(predict_list, "afa")

    return predict_list

