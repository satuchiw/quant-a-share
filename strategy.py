import backtrader as bt

class Strategy_MA(bt.Strategy):
    params = (
        ('ma5_period', 5),
        ('ma20_period', 20),
    )
    def __init__(self):
        self.order = None
        self.buyprice = None
        self.buycomm = None
        self.end_date = self.p.end_date   # access as self.end_date
        self.ma5 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.ma5_period)
        self.ma20 = bt.indicators.SimpleMovingAverage(
            self.data.close, period=self.params.ma20_period)

    def log(self, txt, dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print(f'date:{dt.isoformat()}, {txt}')

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(f'BUY EXECUTED, {order.executed.price:.2f}')
            elif order.issell():
                self.log(f'SELL EXECUTED, {order.executed.price:.2f}')
        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')
        self.order = None

    def next(self):
        if self.order:
            return

        if not self.position:
            if self.data.close[0] > self.ma5[0] and self.ma5[0] > self.ma20[0]:
                self.log(f'BUY CREATE {self.data.close[0]:.2f}')
                self.order = self.buy()
        else:
            if self.data.close[0] < self.ma5[0]:
                self.log(f'SELL CREATE {self.data.close[0]:.2f}')
                self.order = self.sell()

if __name__ == '__main__':
    '''
    以2012年11月30日起贵州茅台10年的股价数据为例，执行双均线策略，起始资金10万元
    '''
    from readdata import *
    from backtest import *  
    start_date = '2012-11-20'
    end_date = '2022-11-20'
    start = '2012-11-20'
    end = '2022-11-20'
    start = datetime.strptime(start, '%Y-%m-%d')
    end = datetime.strptime(end, '%Y-%m-%d')  
    # 转换为datetime对象（用于Backtrader）
    # start='2012-11-20'
    # end='2022-11-20'
    startcash = 100000.0
    freq='d'
    code = "sz.000538"
    login_baostock()
        # 获取股票基本数据
    start_str=str(start_date)
    end_str=str(end_date)
    rs1 = marketinfo(code, start_str, end_str, frequency=freq)
    rs = get_result(rs1)
    # print(rs)

    # 创建数据框并确保所有列都是数值类型
    data = rs[['date', 'open', 'close', 'high', 'low', 'volume']].copy()
    
    # 将价格和交易量列转换为浮点数
    numeric_columns = ['open', 'close', 'high', 'low', 'volume']
    for col in numeric_columns:
        data[col] = data[col].astype(float)
    
    data['date'] = pd.to_datetime(data['date'])
    data = data.set_index('date')
    logout_baostock()
    # 获取股票基本数据
    
    
    # data = import_data_from_csv("D:\\Dataset\\baostocks\\test_data\\600519_day_kline_info.csv")
    cerebro, results = run_backtest(Strategy_MA, data, startcash, start, end)
    
    print(f"初始资金: {startcash}\n回测期间：{start.strftime('%Y%m%d')}:{end.strftime('%Y%m%d')}")
    