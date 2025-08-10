#!/usr/bin/env python3
import backtrader as bt
import pandas as pd
import numpy as np

class DebugStrategy(bt.Strategy):
    """
    Debug strategy to understand portfolio value tracking
    """
    
    def __init__(self):
        self.portfolio_values = []
        self.dates = []
        self.trade_count = 0
        self.last_value = None
        
    def next(self):
        # Get current values
        cash = self.broker.getcash()
        position_size = self.position.size if self.position else 0
        current_price = self.data.close[0]
        position_value = position_size * current_price
        total_value = cash + position_value
        
        current_date = self.datas[0].datetime.date(0)
        
        # Track values
        self.portfolio_values.append(total_value)
        self.dates.append(current_date)
        
        # Debug output every 50 days
        if len(self.portfolio_values) % 50 == 0:
            print(f"Day {len(self.portfolio_values)}: Cash={cash:.2f}, Position={position_size}, "
                  f"Price={current_price:.2f}, PositionValue={position_value:.2f}, "
                  f"Total={total_value:.2f}")
            
            if self.last_value is not None:
                change = total_value - self.last_value
                print(f"  Change: {change:+.2f}")
            
            self.last_value = total_value
        
        # Make a trade every 100 days
        if len(self.portfolio_values) % 100 == 0 and not self.position:
            self.buy()
            self.trade_count += 1
            print(f"TRADE {self.trade_count}: BUY at {current_price:.2f}")
        elif len(self.portfolio_values) % 100 == 50 and self.position:
            self.sell()
            print(f"TRADE {self.trade_count}: SELL at {current_price:.2f}")

def debug_portfolio_tracking():
    """Debug portfolio value tracking"""
    
    # Create test data with more variation
    dates = pd.date_range('2020-01-01', '2021-01-01', freq='D')
    prices = 100 + np.cumsum(np.random.randn(len(dates)) * 2)  # More volatile
    
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
    cerebro.addstrategy(DebugStrategy)
    
    print("Starting Portfolio Value:", cerebro.broker.getvalue())
    results = cerebro.run()
    strat = results[0]
    print("Final Portfolio Value:", cerebro.broker.getvalue())
    
    # Analyze portfolio values
    portfolio_values = strat.portfolio_values
    print(f"\nPortfolio values tracked: {len(portfolio_values)}")
    print(f"Portfolio range: {min(portfolio_values):.2f} to {max(portfolio_values):.2f}")
    
    # Show significant changes
    changes = []
    for i in range(1, len(portfolio_values)):
        change = portfolio_values[i] - portfolio_values[i-1]
        changes.append(change)
        if abs(change) > 1:  # Show significant changes
            print(f"Day {i}: Change = {change:+.2f}")
    
    print(f"\nTotal significant changes: {sum(1 for c in changes if abs(c) > 1)}")
    print(f"Changes range: {min(changes):.6f} to {max(changes):.6f}")

if __name__ == "__main__":
    debug_portfolio_tracking() 