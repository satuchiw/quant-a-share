# from readdata import *
# from strategy import Strategy_MA
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
import backtrader as bt
import math
# %matplotlib widget
# %matplotlib inline

def import_data_from_csv(file_path):
    # 读取现有数据

    columns = ['date','open','close','high', 'low', 'volume'] # 对于backtrader来说只需要这几列数据（还有openinterest暂时先不用）
    data = pd.read_csv(file_path, usecols=columns, parse_dates=True, index_col='date')
    data = data.sort_index()
    
    return data
    
# class Strategy_MA(bt.Strategy):
#     # 均线策略
#     params = (
#                 ('ma5_period', 5),
#                 ('ma20_period', 20) 
#     )  # 设定全局交易策略参数

#     def log(self, txt, dt=None):
#         # 日志记录函数
#         dt = dt or self.datas[0].datetime.date(0)
#         print('date:%s, %s' % (dt.isoformat(), txt))
    
#     def __init__(self):
#         # 初始化交易指令、买卖价格和手续费
#         self.order = None
#         self.buyprice = None
#         self.buycomm = None 
 
#         # 添加移动均线指标，内置了talib模块
#         self.ma5 = bt.indicators.SimpleMovingAverage(
#             self.data.close, period=self.params.ma5_period)
#         self.ma20 = bt.indicators.SimpleMovingAverage(
#             self.data.close, period=self.params.ma20_period)
        
#     def notify_order(self, order):
#         # 处理和打印订单信息
        
#         # 买卖订单已提交/已接受 - 无需操作
#         if order.status in [order.Submitted, order.Accepted]:
#             return
        
#         # 检查订单是否已完成
#         if order.status in [order.Completed]:
#             if order.isbuy():
#                 self.log('买入已执行，%.2f' % order.executed.price) # 记录日志
#             elif order.issell():
#                 self.log('卖出已执行，%.2f' % order.executed.price)
                
#             self.bar_executed = len(self)
            
#         elif order.status in [order.Canceled, order.Margin, order.Rejected]:
#             self.log('订单已取消/保证金不足/拒绝')
            
#         # 记录：没有待处理订单
#         self.order = None
        
#     def notify_trade(self, trade):
#         # 处理和打印交易信息
#         if not trade.isclosed:
#             return

#         self.log(f'本次交易毛利润：{trade.pnl:.2f},扣除交易费用后的净利润：{trade.pnlcomm:.2f}')

#         if trade.pnlcomm > 0:  # 如果净收益大于0，就认为这次交易盈利，否则认为这次交易亏损（同时输出交易编号）
#             self.log(f'交易获利： {trade.ref}')
#         else:
#             self.log(f'交易亏损： {trade.ref}')  

#     def next(self):
#         #主要的循环策略执行部分
        
#         # 当前资产总价`
#         total_value = self.broker.getvalue()
        
#         # 检查是否有待处理订单，如果有就不执行此轮操作
#         if self.order:
#             return
        
#         # 回测最后一天停止交易
#         if self.datas[0].datetime.date(0) == end:
#             return 
        
#         # 这里是九成仓买入卖出的策略
#         if self.position.size:  # 检查当前是否已持仓（因为该策略只有持仓和空仓两种状态）
#             if self.ma5[0] < self.ma20[0] and self.ma5[-1] > self.ma20[-1]:   # 检查是否满足卖出条件
#                 self.log("总资产价格：%.2f元" % total_value) 
#                 print("{:-^50s}".format("Split Line"))
#                 self.log('卖出创建，%.2f' % self.data.close[0])
#                 self.close()
#         elif self.ma5[0] > self.ma20[0] and self.ma5[-1] < self.ma20[-1]:     # 检查是否满足买入条件(此处是否应当用第二天买入价？)
#             order_amount = abs((total_value*0.9/self.datas[0].close[0])//100*100)
#             self.log("总资产价格：%.2f元" % total_value)
#             print("{:-^50s}".format("Split Line"))
#             self.log('买入创建，%.2f' % self.data.close[0])
#             self.buy(self.datas[0], size=order_amount)

def run_backtest(strategy, data, startcash, start, end):
    # 执行回测
    # 实例化Cerebro回测引擎
    cerebro = bt.Cerebro()
    # 添加策略分析指标
    cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='tradeanalyzer') # 平仓交易信息
    cerebro.addanalyzer(bt.analyzers.AnnualReturn, _name='annualReturn') # 年度回报
    cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown') # 回撤
    cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe') # 夏普率
    # 添加数据
    cerebro.adddata(bt.feeds.PandasData(dataname=data,fromdate=start,todate=end))
    # 添加策略
    cerebro.addstrategy(strategy)
    # 设置初始投资总额
    cerebro.broker.setcash(startcash)
    # 设置交易佣金（双边万五）
    cerebro.broker.setcommission(commission=0.0005)
    # 添加观测器
    # cerebro.addobserver(...)
    # 运行回测
    results = cerebro.run()
    
    # 打印分析器输出结果（这样输出很乱，暂时不执行）
    #print('Tradeanalyzer:', results[0].analyzers.tradeanalyzer.get_analysis())
    #print('AnnualReturn:', results[0].analyzers.annualReturn.get_analysis())
    #print('DrawDown:', results[0].analyzers.drawdown.get_analysis())
    #print('SharpeRatio:', results[0].analyzers.sharpe.get_analysis())
    
    return cerebro, results
def evaluate_results(cerebro, results):
    # 交易分析与评价
    
    #获取回测结束后的总资金
    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash
    #打印结果
    print(f'总资金: {round(portvalue,2)}')
    # 净收益
    print(f'净收益: {round(pnl,2)}')
    
def plot_results(cerebro):
    # 交易过程可视化
    
    cerebro.plot(style='candlestick')
def analyze_backtest(cerebro, results):
    """全面分析回测结果"""
    # 获取策略实例
    strat = results[0]
    
    # 打印基本账户信息
    start_val = cerebro.broker.startingcash
    end_val = cerebro.broker.getvalue()
    print(f"初始资金: ¥{start_val:,.2f}")
    print(f"最终资金: ¥{end_val:,.2f}")
    print(f"净收益: ¥{end_val - start_val:,.2f} ({((end_val/start_val)-1)*100:.2f}%)")
    
    # 分析交易统计
    ta = strat.analyzers.tradeanalyzer.get_analysis()
    print("\n===== 交易统计 =====")
    print(f"总交易次数: {ta.total.closed}")
    print(f"盈利交易: {ta.won.total} ({ta.won.total/ta.total.closed*100:.2f}%)")
    print(f"亏损交易: {ta.lost.total} ({ta.lost.total/ta.total.closed*100:.2f}%)")
    print(f"平均盈利: ¥{ta.won.pnl.average:.2f}")
    print(f"平均亏损: ¥{ta.lost.pnl.average:.2f}")
    
    # 分析风险指标
    dd = strat.analyzers.drawdown.get_analysis()
    print("\n===== 风险分析 =====")
    print(f"最大回撤: {dd.max.drawdown:.2f}%")
    print(f"最长回撤周期: {dd.max.len} 天")
    
    # 夏普比率
    sharpe = strat.analyzers.sharpe.get_analysis()
    print(f"年化夏普比率: {sharpe['sharperatio']:.2f}")
    
    # 年度回报
    annual_ret = strat.analyzers.annualReturn.get_analysis()
    print("\n===== 年度回报 =====")
    for year, ret in annual_ret.items():
        print(f"{year}: {ret*100:.2f}%")
    
    # 绘制资金曲线
    plt.figure(figsize=(12, 6))
    plt.plot(strat.equity.array)
    plt.title('资金曲线')
    plt.xlabel('交易日')
    plt.ylabel('账户价值')
    plt.grid(True)
    plt.show()
    
    return {
        'starting_cash': start_val,
        'ending_cash': end_val,
        'total_trades': ta.total.closed,
        'win_rate': ta.won.total/ta.total.closed,
        'max_drawdown': dd.max.drawdown,
        'sharpe_ratio': sharpe['sharperatio']
    }





