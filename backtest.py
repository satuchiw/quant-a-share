import backtrader as bt
import pandas as pd
import json
import os
from datetime import datetime
from data_fetcher import DataFetcher
from strategies import STRATEGIES
from performance_analyzer import PerformanceAnalyzer

class BacktestEngine:
    def __init__(self, start_cash=100000):
        self.start_cash = start_cash

    def run_backtest(self, strategy_cls, df, **kwargs):
        """
        Run backtest with given strategy and data
        
        Args:
            strategy_cls: Strategy class to use
            df: DataFrame with OHLCV data
            **kwargs: Strategy parameters
            
        Returns:
            tuple: (metrics, cerebro, results)
        """
        cerebro = bt.Cerebro()
        cerebro.broker.setcash(self.start_cash)
        datafeed = bt.feeds.PandasData(dataname=df)
        cerebro.adddata(datafeed)
        cerebro.addstrategy(strategy_cls, **kwargs)
        
        # Add analyzers
        cerebro.addanalyzer(bt.analyzers.SharpeRatio, _name='sharpe', timeframe=bt.TimeFrame.Days, riskfreerate=0.0)
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name='drawdown')
        cerebro.addanalyzer(bt.analyzers.Returns, _name='returns')
        cerebro.addanalyzer(bt.analyzers.TradeAnalyzer, _name='trades')
        
        print(f"[INFO] Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
        results = cerebro.run()
        strat = results[0]
        print(f"[INFO] Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
        
        # Collect metrics
        sharpe = strat.analyzers.sharpe.get_analysis()
        drawdown = strat.analyzers.drawdown.get_analysis()
        returns = strat.analyzers.returns.get_analysis()
        trades = strat.analyzers.trades.get_analysis()
        
        def safe_percent(val):
            try:
                return f"{float(val) * 100:.2f}%"
            except (TypeError, ValueError):
                return "N/A"
        
        def safe_float(val):
            try:
                return f"{float(val):.2f}"
            except (TypeError, ValueError):
                return "N/A"
        
        metrics = {
            'sharpe_ratio': safe_float(sharpe.get('sharperatio')),
            'max_drawdown': safe_percent(drawdown.get('max', {}).get('drawdown')),
            'total_return': safe_percent(returns.get('rtot')),
            'annual_return': safe_percent(returns.get('rannual')),
            'total_trades': trades.get('total', {}).get('total', 'N/A'),
            'winning_trades': trades.get('won', {}).get('total', 'N/A'),
            'losing_trades': trades.get('lost', {}).get('total', 'N/A'),
            'longest_win_streak': trades.get('streak', {}).get('won', {}).get('longest', 'N/A'),
            'longest_lose_streak': trades.get('streak', {}).get('lost', {}).get('longest', 'N/A'),
            'final_value': cerebro.broker.getvalue(),
        }
        return metrics, cerebro, results

def load_config(config_file="config.json"):
    """
    Load configuration from JSON file
    
    Args:
        config_file (str): Path to configuration file
        
    Returns:
        dict: Configuration dictionary
    """
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"[INFO] Loaded configuration from {config_file}")
        return config
    except FileNotFoundError:
        print(f"[ERROR] Configuration file {config_file} not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"[ERROR] Invalid JSON in configuration file: {e}")
        return None

def get_strategy_class(strategy_name):
    """
    Get strategy class by name
    
    Args:
        strategy_name (str): Name of the strategy
        
    Returns:
        class: Strategy class or None if not found
    """
    if strategy_name in STRATEGIES:
        return STRATEGIES[strategy_name]
    else:
        print(f"[ERROR] Strategy '{strategy_name}' not found. Available strategies: {list(STRATEGIES.keys())}")
        return None

def main():
    """
    Main function to run backtest based on configuration
    """
    import sys
    
    # Get config file from command line argument, default to config.json
    config_file = "config.json"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    # Load configuration
    config = load_config(config_file)
    if config is None:
        return
    
    # Extract configuration parameters
    stock_code = config.get('stock_code')
    start_date = config.get('start_date')
    end_date = config.get('end_date')
    strategy_name = config.get('strategy')
    initial_cash = config.get('initial_cash', 100000)
    strategy_params = config.get('strategy_params', {})
    data_frequency = config.get('data_frequency', 'd')
    adjustflag = config.get('adjustflag', '2')
    
    print(f"[INFO] Running backtest for {stock_code}")
    print(f"[INFO] Period: {start_date} to {end_date}")
    print(f"[INFO] Strategy: {strategy_name}")
    print(f"[INFO] Initial cash: {initial_cash}")
    
    # Get strategy class
    strategy_cls = get_strategy_class(strategy_name)
    if strategy_cls is None:
        return
    
    # Initialize data fetcher
    fetcher = DataFetcher()
    
    # Generate expected CSV filename
    code_short = stock_code.split('.')[-1]
    expected_csv = f"{code_short}_{start_date}_{end_date}.csv"
    
    # Check if data file exists, if not download it
    if os.path.exists(expected_csv):
        print(f"[INFO] Using existing data file: {expected_csv}")
        df = fetcher.load_data_from_csv(expected_csv)
    else:
        print(f"[INFO] Data file not found. Downloading data for {stock_code}...")
        csv_path = fetcher.fetch_and_save(
            stock_code, start_date, end_date, 
            frequency=data_frequency, adjustflag=adjustflag
        )
        if csv_path:
            df = fetcher.load_data_from_csv(csv_path)
        else:
            print("[ERROR] Failed to download data.")
            return
    
    if df is None or df.empty:
        print("[ERROR] No data available for backtest.")
        return
    
    print(f"[INFO] Data loaded successfully. Shape: {df.shape}")
    print(f"[INFO] Date range: {df.index.min()} to {df.index.max()}")
    
    # Run backtest
    engine = BacktestEngine(start_cash=initial_cash)
    metrics, cerebro, results = engine.run_backtest(strategy_cls, df, **strategy_params)
    
    # Print results
    print("\n" + "="*50)
    print("BACKTEST RESULTS")
    print("="*50)
    for key, value in metrics.items():
        print(f"{key.replace('_', ' ').title()}: {value}")
    print("="*50)
    
    # Plot results
    try:
        cerebro.plot(style='candlestick', volume=True)
        print("[INFO] Backtest plot generated successfully.")
    except Exception as e:
        print(f"[WARNING] Could not generate backtest plot: {e}")
    
    # Generate cumulative returns comparison with CSI300
    try:
        print("\n[INFO] Generating cumulative returns comparison...")
        analyzer = PerformanceAnalyzer()
        analyzer.analyze_performance(
            cerebro, results, strategy_name, stock_code, 
            start_date, end_date
        )
        print("[INFO] Cumulative returns analysis completed.")
    except Exception as e:
        print(f"[WARNING] Could not generate cumulative returns analysis: {e}")
    
    # Cleanup
    fetcher.logout()

if __name__ == "__main__":
    main()





