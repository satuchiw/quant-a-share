import backtrader as bt
import pandas as pd
from data.baostock_probe import download_kline_data

class BacktestEngine:
    def __init__(self, start_cash=100000):
        self.start_cash = start_cash

    def run_backtest(self, strategy_cls, df, **kwargs):
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

# Example moving average strategy
class MAStrategy(bt.Strategy):
    params = (('short_window', 10), ('long_window', 30))
    def __init__(self):
        self.ma_short = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.short_window)
        self.ma_long = bt.indicators.SimpleMovingAverage(self.datas[0].close, period=self.params.long_window)
        self.crossover = bt.indicators.CrossOver(self.ma_short, self.ma_long)
    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy()
        elif self.crossover < 0:
            self.sell()

if __name__ == "__main__":
    # Example usage
    STOCK_CODE = "sh.600600"
    START_DATE = "2020-04-01"
    END_DATE = "2021-04-01"
    CSV_PATH = "600600_SH_2020_2021.csv"
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"[INFO] Loaded data from {CSV_PATH}")
    except FileNotFoundError:
        print(f"[INFO] {CSV_PATH} not found. Downloading data...")
        df = download_kline_data(STOCK_CODE, START_DATE, END_DATE, CSV_PATH)
    if df is not None:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
        df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric, errors='coerce')
        engine = BacktestEngine(start_cash=100000)
        metrics, cerebro, results = engine.run_backtest(MAStrategy, df, short_window=10, long_window=30)
        print("\n===== Performance Metrics =====")
        for k, v in metrics.items():
            print(f"{k}: {v}")
        # Plot earnings curve and trades
        cerebro.plot(style='candlestick')
    else:
        print("[ERROR] No data available for backtest.")





