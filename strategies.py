import backtrader as bt

class MAStrategy(bt.Strategy):
    """
    Moving Average Crossover Strategy
    Buys when short MA crosses above long MA
    Sells when short MA crosses below long MA
    """
    params = (
        ('short_window', 10),
        ('long_window', 30),
    )
    
    def __init__(self):
        self.ma_short = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.short_window)
        self.ma_long = bt.indicators.SimpleMovingAverage(
            self.datas[0].close, period=self.params.long_window)
        self.crossover = bt.indicators.CrossOver(self.ma_short, self.ma_long)
        self.order = None
        self.portfolio_values = []
        self.dates = []
        
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
    
    def get_portfolio_value(self):
        """Calculate current portfolio value including unrealized gains/losses"""
        cash = self.broker.getcash()
        position_value = 0
        
        if self.position:
            # Calculate current market value of position
            current_price = self.data.close[0]
            position_size = self.position.size
            position_value = position_size * current_price
        
        return cash + position_value
        
    def next(self):
        if self.order:
            return
            
        if not self.position:
            if self.crossover > 0:
                # Buy with all available cash
                cash = self.broker.getcash()
                if cash > 0:
                    size = int(cash / self.data.close[0])
                    if size > 0:
                        self.log(f'BUY CREATE {self.data.close[0]:.2f} - {size} shares')
                        self.order = self.buy(size=size)
        elif self.crossover < 0:
            # Sell entire position
            self.log(f'SELL CREATE {self.data.close[0]:.2f} - {self.position.size} shares')
            self.order = self.sell(size=self.position.size)
        
        # Track portfolio value and date at the end of each bar (after potential trades)
        current_value = self.get_portfolio_value()
        current_date = self.datas[0].datetime.date(0)
        
        # Always track portfolio value for proper daily returns calculation
        self.portfolio_values.append(current_value)
        self.dates.append(current_date)
        
        # Debug: Print portfolio value changes every 10 days
        if len(self.portfolio_values) % 10 == 0:
            if len(self.portfolio_values) > 1:
                change = current_value - self.portfolio_values[-2]
                self.log(f'Portfolio value: {current_value:.2f} (change: {change:+.2f})')


class RSIStrategy(bt.Strategy):
    """
    RSI Strategy
    Buys when RSI is oversold (< 30)
    Sells when RSI is overbought (> 70)
    """
    params = (
        ('rsi_period', 14),
        ('oversold', 30),
        ('overbought', 70),
    )
    
    def __init__(self):
        self.rsi = bt.indicators.RSI(self.datas[0].close, period=self.params.rsi_period)
        self.order = None
        self.portfolio_values = []
        self.dates = []
        
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
    
    def get_portfolio_value(self):
        """Calculate current portfolio value including unrealized gains/losses"""
        cash = self.broker.getcash()
        position_value = 0
        
        if self.position:
            # Calculate current market value of position
            current_price = self.data.close[0]
            position_size = self.position.size
            position_value = position_size * current_price
        
        return cash + position_value
        
    def next(self):
        if self.order:
            return
            
        if not self.position:
            if self.rsi[0] < self.params.oversold:
                # Buy with all available cash
                cash = self.broker.getcash()
                if cash > 0:
                    size = int(cash / self.data.close[0])
                    if size > 0:
                        self.log(f'BUY CREATE {self.data.close[0]:.2f} (RSI: {self.rsi[0]:.2f}) - {size} shares')
                        self.order = self.buy(size=size)
        elif self.rsi[0] > self.params.overbought:
            # Sell entire position
            self.log(f'SELL CREATE {self.data.close[0]:.2f} (RSI: {self.rsi[0]:.2f}) - {self.position.size} shares')
            self.order = self.sell(size=self.position.size)
        
        # Track portfolio value and date at the end of each bar (after potential trades)
        current_value = self.get_portfolio_value()
        current_date = self.datas[0].datetime.date(0)
        
        self.portfolio_values.append(current_value)
        self.dates.append(current_date)


class BollingerBandsStrategy(bt.Strategy):
    """
    Bollinger Bands Strategy
    Buys when price touches lower band
    Sells when price touches upper band
    """
    params = (
        ('bb_period', 20),
        ('bb_dev', 2),
    )
    
    def __init__(self):
        self.bb = bt.indicators.BollingerBands(
            self.datas[0].close, 
            period=self.params.bb_period, 
            devfactor=self.params.bb_dev
        )
        self.order = None
        self.portfolio_values = []
        self.dates = []
        
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
    
    def get_portfolio_value(self):
        """Calculate current portfolio value including unrealized gains/losses"""
        cash = self.broker.getcash()
        position_value = 0
        
        if self.position:
            # Calculate current market value of position
            current_price = self.data.close[0]
            position_size = self.position.size
            position_value = position_size * current_price
        
        return cash + position_value
        
    def next(self):
        if self.order:
            return
            
        if not self.position:
            if self.data.close[0] <= self.bb.lines.bot[0]:
                # Buy with all available cash
                cash = self.broker.getcash()
                if cash > 0:
                    size = int(cash / self.data.close[0])
                    if size > 0:
                        self.log(f'BUY CREATE {self.data.close[0]:.2f} (Lower BB: {self.bb.lines.bot[0]:.2f}) - {size} shares')
                        self.order = self.buy(size=size)
        elif self.data.close[0] >= self.bb.lines.top[0]:
            # Sell entire position
            self.log(f'SELL CREATE {self.data.close[0]:.2f} (Upper BB: {self.bb.lines.top[0]:.2f}) - {self.position.size} shares')
            self.order = self.sell(size=self.position.size)
        
        # Track portfolio value and date at the end of each bar (after potential trades)
        current_value = self.get_portfolio_value()
        current_date = self.datas[0].datetime.date(0)
        
        self.portfolio_values.append(current_value)
        self.dates.append(current_date)


# Strategy mapping dictionary
STRATEGIES = {
    'MAStrategy': MAStrategy,
    'RSIStrategy': RSIStrategy,
    'BollingerBandsStrategy': BollingerBandsStrategy,
} 