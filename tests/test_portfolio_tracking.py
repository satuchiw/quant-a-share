#!/usr/bin/env python3
import backtrader as bt
import pandas as pd
import numpy as np

class SimpleTestStrategy(bt.Strategy):
    """
    Simple test strategy to verify portfolio tracking
    """
    
    def __init__(self):
        self.portfolio_values = []
        self.dates = []
        self.trade_count = 0
        
    def next(self):
        # Track portfolio value
        current_value = self.broker.getvalue()
        current_date = self.datas[0].datetime.date(0)
        
        self.portfolio_values.append(current_value)
        self.dates.append(current_date)
        
        # Make a simple trade every 100 days
        if len(self.portfolio_values) % 100 == 0 and not self.position:
            self.buy()
            self.trade_count += 1
            print(f"Trade {self.trade_count}: BUY at {self.data.close[0]:.2f}, Portfolio: {current_value:.2f}")
        elif len(self.portfolio_values) % 100 == 50 and self.position:
            self.sell()
            print(f"Trade {self.trade_count}: SELL at {self.data.close[0]:.2f}, Portfolio: {current_value:.2f}")
        
        # Print significant changes
        if len(self.portfolio_values) > 1:
            change = current_value - self.portfolio_values[-2]
            if abs(change) > 100:  # Significant change
                print(f"Significant change: {change:+.2f} at {current_date}")

def test_portfolio_tracking():
    """Test portfolio value tracking with simple data"""
    
    # Create simple test data
    dates = pd.date_range('2020-01-01', '2021-01-01', freq='D')
    prices = 100 + np.cumsum(np.random.randn(len(dates)) * 0.5)  # Random walk
    
    df = pd.DataFrame({
        'open': prices,
        'high': prices * 1.02,
        'low': prices * 0.98,
        'close': prices,
        'volume': 1000000
    }, index=dates)
    
    # Run backtest
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(100000)
    datafeed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(datafeed)
    cerebro.addstrategy(SimpleTestStrategy)
    
    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    results = cerebro.run()
    strat = results[0]
    print("Final Portfolio Value:", cerebro.broker.getvalue())
    
    # Analyze portfolio values
    portfolio_values = strat.portfolio_values
    print(f"\nPortfolio values tracked: {len(portfolio_values)}")
    print(f"Portfolio range: {min(portfolio_values):.2f} to {max(portfolio_values):.2f}")
    
    # Calculate daily returns
    daily_returns = []
    for i in range(1, len(portfolio_values)):
        if portfolio_values[i-1] > 0:
            daily_return = (portfolio_values[i] - portfolio_values[i-1]) / portfolio_values[i-1]
            daily_returns.append(daily_return)
    
    print(f"Daily returns range: {min(daily_returns):.6f} to {max(daily_returns):.6f}")
    print(f"Non-zero daily returns: {sum(1 for r in daily_returns if abs(r) > 0.0001)}")
    
    # Show some portfolio value changes
    changes = [portfolio_values[i] - portfolio_values[i-1] for i in range(1, min(11, len(portfolio_values)))]
    print(f"First 10 portfolio changes: {[f'{c:+.2f}' for c in changes]}")

if __name__ == "__main__":
    test_portfolio_tracking() 