#!/usr/bin/env python3
import backtrader as bt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json
from data_fetcher import DataFetcher
from strategies import STRATEGIES

def save_strategy_data_to_excel(config_file="config_rsi.json"):
    """
    Run backtest and save strategy data to Excel file
    """
    # Load configuration
    with open(config_file, 'r', encoding='utf-8') as f:
        config = json.load(f)
    
    stock_code = config.get('stock_code')
    start_date = config.get('start_date')
    end_date = config.get('end_date')
    strategy_name = config.get('strategy')
    initial_cash = config.get('initial_cash', 100000)
    strategy_params = config.get('strategy_params', {})
    
    print(f"[INFO] Running backtest for {stock_code}")
    print(f"[INFO] Period: {start_date} to {end_date}")
    print(f"[INFO] Strategy: {strategy_name}")
    
    # Get strategy class
    strategy_cls = STRATEGIES[strategy_name]
    
    # Initialize data fetcher
    fetcher = DataFetcher()
    
    # Generate expected CSV filename
    code_short = stock_code.split('.')[-1]
    expected_csv = f"{code_short}_{start_date}_{end_date}.csv"
    
    # Load data
    if os.path.exists(expected_csv):
        print(f"[INFO] Using existing data file: {expected_csv}")
        df = fetcher.load_data_from_csv(expected_csv)
    else:
        print(f"[ERROR] Data file not found: {expected_csv}")
        return None
    
    if df is None or df.empty:
        print("[ERROR] No data available for backtest.")
        return None
    
    print(f"[INFO] Data loaded successfully. Shape: {df.shape}")
    
    # Run backtest
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(initial_cash)
    datafeed = bt.feeds.PandasData(dataname=df)
    cerebro.adddata(datafeed)
    cerebro.addstrategy(strategy_cls, **strategy_params)
    
    print(f"[INFO] Starting Portfolio Value: {cerebro.broker.getvalue():.2f}")
    results = cerebro.run()
    strat = results[0]
    print(f"[INFO] Final Portfolio Value: {cerebro.broker.getvalue():.2f}")
    
    # Get portfolio values and dates
    portfolio_values = getattr(strat, 'portfolio_values', [])
    dates = getattr(strat, 'dates', [])
    
    if not portfolio_values:
        print("[ERROR] No portfolio values tracked by strategy.")
        return None
    
    # Convert dates to datetime objects
    datetime_dates = []
    for date in dates:
        if isinstance(date, str):
            datetime_dates.append(pd.to_datetime(date))
        elif hasattr(date, 'isoformat'):
            datetime_dates.append(pd.to_datetime(date.isoformat()))
        else:
            datetime_dates.append(pd.to_datetime(date))
    
    # Create DataFrame with strategy data
    strategy_df = pd.DataFrame({
        'Date': datetime_dates,
        'Portfolio_Value': portfolio_values
    })
    
    # Calculate daily returns
    strategy_df['Daily_Return'] = strategy_df['Portfolio_Value'].pct_change()
    
    # Calculate cumulative returns (starting from 1.0)
    strategy_df['Cumulative_Return'] = (1 + strategy_df['Daily_Return']).cumprod()
    
    # Fetch CSI300 data for comparison
    print("[INFO] Fetching CSI300 data for comparison...")
    fetcher.login()
    csi300_data = fetcher.fetch_data("sh.000300", start_date, end_date)
    fetcher.logout()
    
    if csi300_data is not None:
        # Process CSI300 data
        csi300_data['date'] = pd.to_datetime(csi300_data['date'])
        csi300_data['close'] = pd.to_numeric(csi300_data['close'], errors='coerce')
        csi300_data.set_index('date', inplace=True)
        
        # Calculate CSI300 daily returns
        csi300_data['Daily_Return'] = csi300_data['close'].pct_change()
        csi300_data['Cumulative_Return'] = (1 + csi300_data['Daily_Return']).cumprod()
        
        # Merge strategy and CSI300 data
        merged_df = pd.merge(strategy_df, csi300_data[['close', 'Daily_Return', 'Cumulative_Return']], 
                           left_on='Date', right_index=True, how='left')
        merged_df.rename(columns={'close': 'CSI300_Close', 'Daily_Return': 'CSI300_Daily_Return', 
                                'Cumulative_Return': 'CSI300_Cumulative_Return'}, inplace=True)
    else:
        merged_df = strategy_df
    
    # Save to Excel
    excel_filename = f"strategy_data_{strategy_name}_{code_short}_{start_date}_{end_date}.xlsx"
    merged_df.to_excel(excel_filename, index=False)
    print(f"[INFO] Strategy data saved to: {excel_filename}")
    
    return excel_filename, merged_df

def plot_from_excel(excel_filename):
    """
    Plot cumulative returns from Excel data using pandas
    """
    # Read data from Excel
    df = pd.read_excel(excel_filename)
    df['Date'] = pd.to_datetime(df['Date'])
    
    print(f"[INFO] Loaded data from Excel: {len(df)} rows")
    print(f"[INFO] Date range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"[INFO] Portfolio value range: {df['Portfolio_Value'].min():.2f} to {df['Portfolio_Value'].max():.2f}")
    print(f"[INFO] Cumulative return range: {df['Cumulative_Return'].min():.4f} to {df['Cumulative_Return'].max():.4f}")
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    # Plot strategy cumulative returns
    plt.plot(df['Date'], df['Cumulative_Return'], 
             label='Strategy (RSI)', linewidth=2, color='blue')
    
    # Plot CSI300 cumulative returns if available
    if 'CSI300_Cumulative_Return' in df.columns:
        plt.plot(df['Date'], df['CSI300_Cumulative_Return'], 
                label='CSI300 Index', linewidth=2, color='red', linestyle='--')
    
    # Customize the plot
    plt.title('Cumulative Returns Comparison: Strategy vs CSI300', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (Base = 100%)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=6))
    plt.xticks(rotation=45)
    
    # Add performance metrics
    final_strategy_return = (df['Cumulative_Return'].iloc[-1] - 1) * 100
    plt.text(0.02, 0.98, f'Final Strategy Return: {final_strategy_return:.2f}%', 
             transform=plt.gca().transAxes, fontsize=10, 
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    if 'CSI300_Cumulative_Return' in df.columns:
        final_benchmark_return = (df['CSI300_Cumulative_Return'].iloc[-1] - 1) * 100
        plt.text(0.02, 0.92, f'Final CSI300 Return: {final_benchmark_return:.2f}%', 
                transform=plt.gca().transAxes, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.8))
        
        # Calculate outperformance
        outperformance = final_strategy_return - final_benchmark_return
        color = 'green' if outperformance > 0 else 'red'
        plt.text(0.02, 0.86, f'Outperformance: {outperformance:+.2f}%', 
                transform=plt.gca().transAxes, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor=color, alpha=0.8))
    
    plt.tight_layout()
    plt.show()
    
    # Print summary statistics
    print("\n" + "="*60)
    print("CUMULATIVE RETURNS ANALYSIS (FROM EXCEL)")
    print("="*60)
    print(f"Strategy: RSIStrategy")
    print(f"Stock: sh.600600")
    print(f"Final Strategy Return: {final_strategy_return:.2f}%")
    
    if 'CSI300_Cumulative_Return' in df.columns:
        print(f"Final CSI300 Return: {final_benchmark_return:.2f}%")
        print(f"Outperformance: {outperformance:+.2f}%")
    
    print("="*60)

if __name__ == "__main__":
    import os
    
    # Save strategy data to Excel
    excel_file, data_df = save_strategy_data_to_excel()
    
    if excel_file:
        # Plot from Excel data
        plot_from_excel(excel_file)
        
        # Show some sample data
        print("\nSample data from Excel:")
        print(data_df.head(10))
        print("\nLast 5 rows:")
        print(data_df.tail())
    else:
        print("Failed to save strategy data to Excel.") 