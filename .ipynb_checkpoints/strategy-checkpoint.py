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

