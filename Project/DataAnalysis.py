import numpy as np
import pandas as pd
import fbprophet as Prophet
import sklearn
from fbprophet.plot import plot_yearly, seasonality_plot_df, set_y_as_percent
import joblib
import time
from statsmodels.tsa.stattools import adfuller

# v1：用于数据预测和生成数据趋势
# 输入：一个表，一列为时间，一列为为某个传感器类型下某个传感器的某段时间的数据
# 输出:该传感器对应的趋势值（分为日内趋势、年内趋势、总趋势）、预测值
# 输出的格式均为字典，索引为时间，跟着个列表，若为趋势值，列表的元素为['trend', 'trend_lower', 'trend_upper']，代表趋势、趋势的下限和趋势的上限
# 若为预测值，列表的元素为['yhat', 'yhat_lower', 'yhat_upper']，代表预测值、预测值的下限和预测值的上限
import config


def dataPreview(sensor_data, periods):  # 数据预测
    m = createFbprophet(sensor_data)
    forecast_list = list()

    future = m.make_future_dataframe(periods=50, freq=periods)
    forecast = m.predict(future)
    forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    forecast = forecast.rename(columns={'ds': '时间'})
    forecast = forecast.iloc[-periods:]
    forecast = forecast.reset_index(drop=True)
    for i in range(0, len(forecast)):
        part = forecast.loc[i].T.to_dict()
        forecast_list.append(part)
    print(forecast_list)
    return forecast_list


def dataTrend(sensor_data):  # 数据总趋势
    m = createFbprophet(sensor_data)
    forecast_list = []
    future = m.make_future_dataframe(periods=0)
    forecast = m.predict(future)
    forecast = forecast[['ds', 'trend', 'trend_lower', 'trend_upper']]
    forecast = forecast.rename(columns={'ds': '时间'})
    forecast = forecast.reset_index(drop=True)
    for i in range(0, len(forecast)):
        forecast.loc[i, 1] = round(forecast.loc[i, 1], 4)
        forecast.loc[i, 2] = round(forecast.loc[i, 2], 4)
        forecast.loc[i, 3] = round(forecast.loc[i, 3], 4)
        part = forecast.loc[i].T.to_dict()
        forecast_list.append(part)
    print(forecast_list)
    return forecast_list


def dailySeasonality(sensor_data, name='daily'):  # 数据日内趋势，日内趋势需要一整天的数据
    time_list = []
    data_daily_season_list = []
    m = createFbprophet(sensor_data)
    start = pd.to_datetime('2017-01-01 0000')
    period = m.seasonalities[name]['period']
    end = start + pd.Timedelta(days=period)
    plot_points = 200
    days = pd.to_datetime(np.linspace(start.value, end.value, plot_points))
    df_y = Prophet.plot.seasonality_plot_df(m, days)
    seas = m.predict_seasonal_components(df_y)
    for da in df_y['ds'].dt.to_pydatetime():
        time_list.append(da.strftime("%H:%M:%S"))
    data_daily_season = pd.DataFrame(data=time_list, columns=['时间'])
    data_daily_season['数据'] = seas[name]
    data_daily_season.drop(data_daily_season.tail(1).index, inplace=True)
    data_daily_season = data_daily_season.reset_index(drop=True)
    for i in range(0, len(data_daily_season)):
        part = data_daily_season.loc[i].T.to_dict()
        data_daily_season_list.append(part)
    print(data_daily_season_list)
    return data_daily_season_list


def yearlySeasonality(sensor_data, yearly_start=0):  # 数据年内趋势，可能有误。年内趋势需要一整年的数据
    data_yearly_season_list = []
    sensor_data['时间'] = pd.to_datetime(sensor_data['时间'], format='%Y-%m-%d %H:%M:%S')  # 4位年用Y，2位年用y
    data = sensor_data.rename(columns={'时间': 'ds', sensor_data.columns[1]: 'y'})
    data['ds'] = pd.to_datetime(data['ds'], unit='s')
    m = Prophet.Prophet(yearly_seasonality=True)
    m.fit(data)
    time_list = []
    days = (pd.date_range(start='2017-01-01', periods=365) +
            pd.Timedelta(days=yearly_start))
    df_y = Prophet.plot.seasonality_plot_df(m, days)
    seas = m.predict_seasonal_components(df_y)
    for da in df_y['ds'].dt.to_pydatetime():
        time_list.append(da.strftime("%b"))
    data_yearly_season = pd.DataFrame(data=time_list, columns=['时间'])
    data_yearly_season['数据'] = seas['yearly']
    data_yearly_season.drop(data_yearly_season.tail(1).index, inplace=True)
    data_yearly_season = data_yearly_season.reset_index(drop=True)
    for i in range(0, len(data_yearly_season)):
        part = data_yearly_season.loc[i].T.to_dict()
        data_yearly_season_list.append(part)
    print(data_yearly_season_list)
    return data_yearly_season_list


def createFbprophet(sensor_data):  # 创建预测对象
    sensor_data['时间'] = pd.to_datetime(sensor_data['时间'], format='%Y-%m-%d %H:%M:%S')  # 4位年用Y，2位年用y
    data = sensor_data.rename(columns={'时间': 'ds', sensor_data.columns[1]: 'y'})
    data['ds'] = pd.to_datetime(data['ds'], unit='s')
    m = Prophet.Prophet()
    m.fit(data)
    return m



# v1：计算数据的平稳性
# 输入：这里的data应该是限定了时间范围和传感器型号后，数据库执行查询命令，返给我的一个表格，一列是时间，一列是传感器值
# 输出：输出的话是数据的稳定状态，是string格式。将string直接存入数据库中。前端提取数据库中最新的string


def testStationarity(data):
    data = data.iloc[:, 1]
    stationary = adfuller(data)[1]
    if stationary > 0.5:
        report = '数据非常不稳定'
    elif stationary > 0.3:
        report = '数据不稳定'
    elif stationary > 0.15:
        report = '数据不稳定程度较低'
    else:
        report = '数据稳定'
    return report






# 调用示例
# 加载数据
# data = dataProcessedSave(data_old)
# createFbprophet(data,"压力检测","A1")
# 数据预测
# data_preview = dataPreview(10, "压力检测", "A1")  # 预测将来100个时间间隔的数据
# 数据总趋势
# data_trend = dataTrend(data)
# 计算日内趋势
# data_daily_season = dailySeasonality(data)
# 计算年内趋势
# data_yearly_season = yearlySeasonality(data)
