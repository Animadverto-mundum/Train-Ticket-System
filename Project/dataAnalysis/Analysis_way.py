import numpy as np
import pandas as pd
# import fbprophet as Prophet
import sklearn
# from fbprophet.plot import plot_yearly, seasonality_plot_df, set_y_as_percent
import joblib
import time
from statsmodels.tsa.stattools import adfuller


def dataPreview(sensor_data, periods):  # 数据预测,periods为预测间隔
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


def yearlySeasonality(sensor_data, yearly_start=0):  # 数据年内趋势，可能有误。年内趋势需要一整年的数据
    data_yearly_season_list = []
    m=createFbprophet(sensor_data,yearly_seasonality=True)
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


def createFbprophet(sensor_data,yearly_seasonality=False):  # 创建预测对象
    sensor_data['时间'] = pd.to_datetime(sensor_data['时间'], format='%Y-%m-%d %H:%M:%S')  # 4位年用Y，2位年用y
    data = sensor_data.rename(columns={'时间': 'ds', sensor_data.columns[1]: 'y'})
    data['ds'] = pd.to_datetime(data['ds'], unit='s')
    # 添加节假日
    holidays = pd.DataFrame({
        'holiday': '节假日',
        'ds': pd.to_datetime(
            ['2020-01-01', '2020-01-04', '2020-01-05', '2020-01-11', '2020-01-12', '2020-01-18', '2020-01-24',
             '2020-01-25', '2020-01-26', '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31',
             '2020-02-01', '2020-02-02', '2020-02-08', '2020-02-09', '2020-02-15', '2020-02-16', '2020-02-22',
             '2020-02-23', '2020-02-29', '2020-03-01', '2020-03-07', '2020-03-08', '2020-03-14', '2020-03-15',
             '2020-03-21', '2020-03-22', '2020-03-28', '2020-03-29', '2020-04-04', '2020-04-05', '2020-04-06',
             '2020-04-11', '2020-04-12', '2020-04-18', '2020-04-19', '2020-04-25', '2020-05-01', '2020-05-02',
             '2020-05-03', '2020-05-05', '2020-05-10', '2020-05-16', '2020-05-17', '2020-05-23', '2020-05-24',
             '2020-05-30', '2020-05-31', '2020-06-06', '2020-06-07', '2020-06-13', '2020-06-14', '2020-06-20',
             '2020-06-21', '2020-06-25', '2020-06-26', '2020-06-27', '2020-07-04', '2020-07-05', '2020-07-11',
             '2020-07-12', '2020-07-18', '2020-07-19', '2020-07-25', '2020-07-26', '2020-08-01', '2020-08-02',
             '2020-08-08', '2020-08-09', '2020-08-15', '2020-08-16', '2020-08-22', '2020-08-23', '2020-08-29',
             '2020-08-30', '2020-09-05', '2020-09-06', '2020-09-12', '2020-09-13', '2020-09-19', '2020-09-20',
             '2020-09-26', '2020-10-01', '2020-10-02', '2020-10-03', '2020-10-04', '2020-10-05', '2020-10-06',
             '2020-10-07', '2020-10-08', '2020-10-11', '2020-10-17', '2020-10-18', '2020-10-24', '2020-10-25',
             '2020-10-31', '2020-11-01', '2020-11-07', '2020-11-08', '2020-11-14', '2020-11-15', '2020-11-21',
             '2020-11-22', '2020-11-28', '2020-11-29', '2020-12-05', '2020-12-06', '2020-12-12', '2020-12-13',
             '2020-12-19', '2020-12-20', '2020-12-26', '2020-12-27']),
        'lower_window': -1,
        'upper_window': 0,
    })
    m = Prophet.Prophet(holidays=holidays,yearly_seasonality=yearly_seasonality)
    m.fit(data)
    return m


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
