import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import baostock as bs
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class PerformanceAnalyzer:
    """
    Performance analyzer for backtest results with CSI300 comparison
    """
    
    def __init__(self):
        self.csi300_data = None
        
    def fetch_csi300_data(self, start_date, end_date):
        """
        Fetch CSI300 index data for comparison
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            
        Returns:
            pandas.DataFrame: CSI300 data
        """
        print("[INFO] Fetching CSI300 data for comparison...")
        
        # Login to Baostock
        lg = bs.login()
        if lg.error_code != '0':
            print(f"[ERROR] Baostock login failed: {lg.error_msg}")
            return None
            
        try:
            # Query CSI300 data (CSI300 index code: sh.000300)
            rs = bs.query_history_k_data_plus(
                "sh.000300",
                "date,close",
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="2"
            )
            
            if rs.error_code != '0':
                print(f"[ERROR] CSI300 query failed: {rs.error_msg}")
                return None
                
            # Process data
            data_list = []
            while (rs.error_code == '0') & rs.next():
                data_list.append(rs.get_row_data())
                
            if not data_list:
                print("[WARNING] No CSI300 data returned.")
                return None
                
            # Create DataFrame
            df = pd.DataFrame(data_list, columns=rs.fields)
            df['date'] = pd.to_datetime(df['date'])
            df['close'] = pd.to_numeric(df['close'], errors='coerce')
            df.set_index('date', inplace=True)
            
            print(f"[INFO] CSI300 data loaded: {len(df)} records")
            return df
            
        finally:
            bs.logout()
    
    def calculate_cumulative_returns(self, portfolio_values, benchmark_data=None):
        """
        Calculate cumulative returns for portfolio and benchmark
        
        Args:
            portfolio_values (list): List of portfolio values over time
            benchmark_data (pandas.DataFrame): Benchmark data (CSI300)
            
        Returns:
            tuple: (portfolio_returns, benchmark_returns)
        """
        if not portfolio_values or len(portfolio_values) < 2:
            print("[ERROR] Insufficient portfolio values for calculation")
            return [1.0], None
        
        # Calculate daily returns from portfolio values
        daily_returns = []
        for i in range(1, len(portfolio_values)):
            if portfolio_values[i-1] > 0:  # Avoid division by zero
                daily_return = (portfolio_values[i] - portfolio_values[i-1]) / portfolio_values[i-1]
                daily_returns.append(daily_return)
            else:
                daily_returns.append(0.0)
        
        # Calculate cumulative returns starting from 100%
        cumulative_portfolio = [1.0]  # Start at 100%
        for daily_return in daily_returns:
            cumulative_portfolio.append(cumulative_portfolio[-1] * (1 + daily_return))
        
        print(f"[INFO] Portfolio values range: {min(portfolio_values):.2f} to {max(portfolio_values):.2f}")
        print(f"[INFO] Daily returns range: {min(daily_returns):.4f} to {max(daily_returns):.4f}")
        print(f"[INFO] Cumulative returns range: {min(cumulative_portfolio):.2f} to {max(cumulative_portfolio):.2f}")
        
        # Calculate benchmark returns if available
        cumulative_benchmark = None
        if benchmark_data is not None and not benchmark_data.empty:
            try:
                # Calculate benchmark daily returns
                benchmark_daily_returns = benchmark_data['close'].pct_change().dropna()
                
                # Calculate cumulative benchmark returns
                cumulative_benchmark = [1.0]  # Start at 100%
                for daily_return in benchmark_daily_returns:
                    cumulative_benchmark.append(cumulative_benchmark[-1] * (1 + daily_return))
                
                # Align with portfolio data length
                if len(cumulative_benchmark) > len(cumulative_portfolio):
                    cumulative_benchmark = cumulative_benchmark[:len(cumulative_portfolio)]
                elif len(cumulative_benchmark) < len(cumulative_portfolio):
                    # Pad with last value
                    last_val = cumulative_benchmark[-1] if cumulative_benchmark else 1.0
                    while len(cumulative_benchmark) < len(cumulative_portfolio):
                        cumulative_benchmark.append(last_val)
                
                print(f"[INFO] Benchmark daily returns range: {min(benchmark_daily_returns):.4f} to {max(benchmark_daily_returns):.4f}")
                print(f"[INFO] Benchmark cumulative returns range: {min(cumulative_benchmark):.2f} to {max(cumulative_benchmark):.2f}")
            except Exception as e:
                print(f"[WARNING] Error calculating benchmark returns: {e}")
                cumulative_benchmark = None
        
        return cumulative_portfolio, cumulative_benchmark
    
    def plot_cumulative_returns(self, portfolio_values, dates, benchmark_data=None, 
                               strategy_name="Strategy", stock_code="Unknown"):
        """
        Plot cumulative returns comparison
        
        Args:
            portfolio_values (list): Portfolio values over time
            dates (list): Date list (should be datetime objects)
            benchmark_data (pandas.DataFrame): CSI300 data
            strategy_name (str): Name of the strategy
            stock_code (str): Stock code being tested
        """
        # Calculate cumulative returns
        cumulative_portfolio, cumulative_benchmark = self.calculate_cumulative_returns(
            portfolio_values, benchmark_data
        )
        
        # Create the plot
        plt.figure(figsize=(14, 8))
        
        # Ensure dates are datetime objects
        if len(dates) != len(cumulative_portfolio):
            print(f"[WARNING] Date mismatch: {len(dates)} dates vs {len(cumulative_portfolio)} values")
            # Use index numbers if dates don't match
            x_axis = range(len(cumulative_portfolio))
            x_label = 'Trading Days'
        else:
            x_axis = dates
            x_label = 'Date'
        
        # Plot portfolio returns
        plt.plot(x_axis, cumulative_portfolio, label=f'{strategy_name} ({stock_code})', 
                linewidth=2, color='blue')
        
        # Plot benchmark returns if available
        if cumulative_benchmark and len(cumulative_benchmark) == len(cumulative_portfolio):
            plt.plot(x_axis, cumulative_benchmark, label='CSI300 Index', 
                    linewidth=2, color='red', linestyle='--')
        
        # Customize the plot
        plt.title(f'Cumulative Returns Comparison: {strategy_name} vs CSI300', 
                 fontsize=14, fontweight='bold')
        plt.xlabel(x_label, fontsize=12)
        plt.ylabel('Cumulative Return (Base = 100%)', fontsize=12)
        plt.legend(fontsize=11)
        plt.grid(True, alpha=0.3)
        
        # Format x-axis if using dates
        if x_label == 'Date':
            plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
            plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=2))
            plt.xticks(rotation=45)
        
        # Add performance metrics
        final_portfolio_return = (cumulative_portfolio[-1] - 1) * 100
        plt.text(0.02, 0.98, f'Final Portfolio Return: {final_portfolio_return:.2f}%', 
                transform=plt.gca().transAxes, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
        
        if cumulative_benchmark:
            final_benchmark_return = (cumulative_benchmark[-1] - 1) * 100
            plt.text(0.02, 0.92, f'Final CSI300 Return: {final_benchmark_return:.2f}%', 
                    transform=plt.gca().transAxes, fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.8))
            
            # Calculate outperformance
            outperformance = final_portfolio_return - final_benchmark_return
            color = 'green' if outperformance > 0 else 'red'
            plt.text(0.02, 0.86, f'Outperformance: {outperformance:+.2f}%', 
                    transform=plt.gca().transAxes, fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8))
        
        plt.tight_layout()
        plt.show()
        
        # Print summary statistics
        print("\n" + "="*60)
        print("CUMULATIVE RETURNS ANALYSIS")
        print("="*60)
        print(f"Strategy: {strategy_name}")
        print(f"Stock: {stock_code}")
        print(f"Final Portfolio Return: {final_portfolio_return:.2f}%")
        
        if cumulative_benchmark:
            print(f"Final CSI300 Return: {final_benchmark_return:.2f}%")
            print(f"Outperformance: {outperformance:+.2f}%")
            
            # Calculate additional metrics
            portfolio_volatility = np.std(cumulative_portfolio) * np.sqrt(252) * 100
            benchmark_volatility = np.std(cumulative_benchmark) * np.sqrt(252) * 100
            print(f"Portfolio Volatility: {portfolio_volatility:.2f}%")
            print(f"CSI300 Volatility: {benchmark_volatility:.2f}%")
            
            # Sharpe ratio approximation
            if portfolio_volatility > 0:
                sharpe_ratio = final_portfolio_return / portfolio_volatility
                print(f"Sharpe Ratio: {sharpe_ratio:.2f}")
        
        print("="*60)
    
    def analyze_performance(self, cerebro, results, strategy_name, stock_code, 
                          start_date, end_date):
        """
        Complete performance analysis with CSI300 comparison
        
        Args:
            cerebro: Backtrader cerebro object
            results: Backtrader results
            strategy_name (str): Name of the strategy
            stock_code (str): Stock code
            start_date (str): Start date
            end_date (str): End date
        """
        # Get portfolio values from strategy
        strat = results[0]
        portfolio_values = getattr(strat, 'portfolio_values', [])
        dates = getattr(strat, 'dates', [])
        
        # If strategy doesn't track values, reconstruct from cerebro
        if not portfolio_values:
            print("[INFO] Reconstructing portfolio values from cerebro...")
            portfolio_values = []
            dates = []
            
            # Get initial cash
            initial_cash = cerebro.broker.startingcash
            
            # Reconstruct portfolio values by running the strategy again
            cerebro_temp = bt.Cerebro()
            cerebro_temp.broker.setcash(initial_cash)
            
            # Add the same data and strategy
            datafeed = cerebro.datas[0]
            cerebro_temp.adddata(datafeed)
            cerebro_temp.addstrategy(type(strat), **strat.params._getdict())
            
            # Run to get portfolio values
            results_temp = cerebro_temp.run()
            strat_temp = results_temp[0]
            
            portfolio_values = strat_temp.portfolio_values
            dates = strat_temp.dates
        
        # Convert dates to datetime objects if they're not already
        datetime_dates = []
        for date in dates:
            if isinstance(date, str):
                datetime_dates.append(pd.to_datetime(date))
            elif hasattr(date, 'isoformat'):
                datetime_dates.append(pd.to_datetime(date.isoformat()))
            else:
                datetime_dates.append(pd.to_datetime(date))
        
        print(f"[INFO] Portfolio values tracked: {len(portfolio_values)} points")
        print(f"[INFO] Date range: {datetime_dates[0]} to {datetime_dates[-1]}")
        
        # Debug: Show some portfolio value changes
        if len(portfolio_values) > 10:
            print(f"[DEBUG] First 5 portfolio values: {portfolio_values[:5]}")
            print(f"[DEBUG] Last 5 portfolio values: {portfolio_values[-5:]}")
            changes = [portfolio_values[i] - portfolio_values[i-1] for i in range(1, min(6, len(portfolio_values)))]
            print(f"[DEBUG] Portfolio value changes: {changes}")
        
        # Fetch CSI300 data
        csi300_data = self.fetch_csi300_data(start_date, end_date)
        
        # Plot cumulative returns
        self.plot_cumulative_returns(
            portfolio_values, datetime_dates, csi300_data, 
            strategy_name, stock_code
        )


if __name__ == "__main__":
    # Example usage
    analyzer = PerformanceAnalyzer()
    
    # Test CSI300 data fetching
    start_date = "2020-04-01"
    end_date = "2021-04-01"
    
    csi300_data = analyzer.fetch_csi300_data(start_date, end_date)
    if csi300_data is not None:
        print(f"CSI300 data shape: {csi300_data.shape}")
        print(f"Date range: {csi300_data.index.min()} to {csi300_data.index.max()}") 