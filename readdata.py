#!/usr/bin/env python
# coding: utf-8

# In[48]:


import baostock as bs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplfinance as mpf
import datetime

def login_baostock():
    # 登录系统

    lg = bs.login()
    print('login respond error_code:'+lg.error_code)
    print('login respond error_msg:'+lg.error_msg)

def marketinfo(code, start_date, end_date, frequency="d", adjustflag="3"):
    """code startdate enddate frequency=d,ajustflag=3"""
    # 获取历史K线数据

    if frequency == 'd':  # 非日频数据只记录每个时间段末的价格，w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟
        fields = "date,open,high,low,close,preclose,volume,amount,turn,pctChg,peTTM,pbMRQ"
    else:
        fields = "date,close,volume,amount,turn,pctChg"
    rs = bs.query_history_k_data_plus(code=code,
        fields=fields,  
        start_date=start_date, end_date=end_date,    
        frequency=frequency, adjustflag=adjustflag)   
        # adjustflag 复权类型，默认不复权：3；后复权；1；前复权：2
    print('query_history_k_data_plus respond error_code:'+rs.error_code)
    print('query_history_k_data_plus respond error_msg:'+rs.error_msg)
    return rs

def profitinfo(code, year, quarter):
    # 获取个股季频盈利能力数据（还可获取季频营运和偿债能力等各类数据，在这里不重复列举）

    profit_list = []
    rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
    while (rs_profit.error_code == '0') & rs_profit.next():
        profit_list.append(rs_profit.get_row_data())
    result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)
    return result_profit

def get_result(rs):
    # 打印数据结果

    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    result = pd.DataFrame(data_list, columns=rs.fields)
    return result

def get_fig(result, im_type='candle'):
    # 绘制可视化图表

    data_kline = result.loc[:,('date','open','high','low','close','volume')]
    data_kline.columns = ['Date','Open','High','Low','Close','Volume']
    data_kline.index = pd.DatetimeIndex(data_kline['Date'])
    data_kline[['Open','High','Low','Close','Volume']] = data_kline[['Open','High','Low','Close','Volume']].apply(pd.to_numeric)
    if im_type == 'candle':
        mpf.plot(data_kline, type='candle', volume=True, style='yahoo', mav= (5, 10, 20,30))
    elif im_type == 'line':
        mpf.plot(data_kline, type='line')

def save_to_csv(result, code, frequency, path="C:\\Users\\Rui Ma\\Desktop\\quant\\data\\"):
    # 将获取的个股K线数据保存到本地

    if frequency == 'd':
        freq = 'day'
    elif frequency == 'w':
        freq = 'week'
    else:
        freq = 'month'
    name = code[-6:] + '_' + freq + '_kline_info.csv'
    result.to_csv(path + name, index=False)

def save_profit_to_csv(result_profit, path="C:\\Users\\Rui Ma\\Desktop\\quant\\data\\"):
    # 保存季频指标

    name = code[-6:] + '_profit_info.csv'
    result_profit.to_csv(path + name, encoding="gbk", index=False)

def logout_baostock():
    # 退出登录

    bs.logout()


# In[ ]:


if __name__ == '__main__' :
    
    # 参数设置
    code = "sz.002415"   # 以海康为例
    start_date = '2025-01-01'
    date_today = datetime.datetime.now().strftime('%Y-%m-%d') # 当前日期2023年8月13日
    end_date = date_today
    freq = "d"
    ending_year = 2023
    login_baostock()

    rs1 = marketinfo(code, start_date, end_date)

    rs=get_result(rs1)
    data=rs[['date', 'open', 'close', 'high', 'low', 'volume']].copy()
    data=rs[['date', 'open', 'close', 'high', 'low', 'volume']].copy()

    logout_baostock()


    # 获取企业各类季频数据(以季频盈利能力数据为例，获取从设置日期开始往前5年的数据)
    result_profit = profitinfo(code, ending_year, 4)
    result_profit = result_profit.drop(index=result_profit.index)   
    
    for i in range(5):
        for j in range(4):
            temp = profitinfo(code, ending_year-i, 4-j)
            result_profit = pd.concat([result_profit,temp])
    
    save_to_csv(result_kline, code, frequency=freq)    # 保存个股基本数据
    save_profit_to_csv(result_profit, path="C:\\Users\\Rui Ma\\Desktop\\quant\\data\\")     # 保存季度盈利数据

    get_fig(result_kline)


