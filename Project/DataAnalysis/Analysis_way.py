import numpy as np
import pandas as pd

# import sklearn
from fbprophet.plot import plot_yearly, seasonality_plot_df, set_y_as_percent
import joblib
import time
from statsmodels.tsa.stattools import adfuller
from fbprophet import Prophet
from matplotlib import pyplot as plt
from statsmodels.tsa.stattools import adfuller


def dataPreview(sensor_data, periods,freq):  # 数据预测,periods为预测间隔
    m = createFbprophet(sensor_data)
    forecast_list = list()
    future = m.make_future_dataframe(periods=periods, freq=freq)
    forecast = m.predict(future)
    pic=m.plot(forecast)
    forecast = round(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']])
    forecast = forecast.rename(columns={'ds': '时间'})
    print(forecast)
    forecast = forecast.iloc[-50:]
    forecast = forecast.reset_index(drop=True)
    for i in range(0, len(forecast)):
        part = forecast.loc[i].T.to_dict()
        forecast_list.append(part)
    print(forecast_list)
    return forecast_list,pic


def dataTrend(sensor_data):  # 数据总趋势
    m = createFbprophet(sensor_data,yearly_seasonality=True)
    forecast_list = []
    future = m.make_future_dataframe(periods=0)
    forecast = m.predict(future)
    pic=m.plot_components(forecast)
    forecast = forecast[['ds', 'trend', 'trend_lower', 'trend_upper']]
    forecast = forecast.rename(columns={'ds': '时间'})
    forecast = forecast.reset_index(drop=True)
    # print(forecast)
    for i in range(0, len(forecast)):
        part = forecast.loc[i].T.to_dict()
        forecast_list.append(part)

    return forecast_list,pic


def yearlySeasonality(sensor_data, yearly_start=0):  # 数据年内趋势，可能有误。年内趋势需要一整年的数据
    data_yearly_season_list = []
    m = createFbprophet(sensor_data, yearly_seasonality=True)
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


def createFbprophet(sensor_data, yearly_seasonality=False):  # 创建预测对象
    sensor_data['时间'] = pd.to_datetime(sensor_data['时间'], format='%Y-%m-%d %H:%M:%S')  # 4位年用Y，2位年用y
    data = sensor_data.rename(columns={'时间': 'ds', sensor_data.columns[1]: 'y'})
    data['ds'] = pd.to_datetime(data['ds'], unit='s')
    # 添加节假日
    holidays = pd.DataFrame({
        'holiday': '节假日',
        'ds': pd.to_datetime(
            ['2008','2012']),
        'lower_window': 0,
        'upper_window': 0,
    })
    m = Prophet(holidays=holidays, yearly_seasonality=yearly_seasonality)
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


