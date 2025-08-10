#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import baostock as bs
import sys
import os

def fetch_and_plot_kline():
    """Fetch stock data and plot K-line chart"""
    
    # Configuration
    stock_code = "sh.600600"
    start_date = "2021-02-01"
    end_date = "2021-08-01"
    
    print(f"[INFO] Fetching K-line data for {stock_code}")
    print(f"[INFO] Period: {start_date} to {end_date}")
    
    # Login to Baostock
    print("[INFO] Logging in to Baostock...")
    lg = bs.login()
    if lg.error_code != '0':
        print(f'[ERROR] Login failed: {lg.error_msg}')
        return
    
    print("[INFO] Login successful.")
    
    # Query historical K data
    print(f"[INFO] Querying historical K data for {stock_code} from {start_date} to {end_date}...")
    rs = bs.query_history_k_data_plus(
        stock_code,
        "date,open,high,low,close,volume",
        start_date=start_date,
        end_date=end_date,
        frequency="d",
        adjustflag="2"
    )
    
    if rs.error_code != '0':
        print(f'[ERROR] Query failed: {rs.error_msg}')
        bs.logout()
        return
    
    print("[INFO] Query successful. Processing data...")
    
    # Convert to DataFrame
    data_list = []
    while (rs.error_code == '0') & rs.next():
        data_list.append(rs.get_row_data())
    
    df = pd.DataFrame(data_list, columns=rs.fields)
    
    # Convert data types
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    df['date'] = pd.to_datetime(df['date'])
    
    # Logout
    bs.logout()
    
    print(f"[INFO] Data loaded successfully. Shape: {df.shape}")
    print(f"[INFO] Date range: {df['date'].min()} to {df['date'].max()}")
    print(f"[INFO] Price range: {df['low'].min():.2f} to {df['high'].max():.2f}")
    
    # Plot K-line chart
    plt.figure(figsize=(15, 8))
    
    # Plot candlestick chart
    for i, row in df.iterrows():
        date = row['date']
        open_price = row['open']
        high = row['high']
        low = row['low']
        close = row['close']
        
        # Determine color based on open/close
        color = 'red' if close > open_price else 'green'
        
        # Plot the body
        plt.bar(date, close - open_price, bottom=min(open_price, close), 
                color=color, alpha=0.7, width=0.8)
        
        # Plot the wick
        plt.plot([date, date], [low, high], color='black', linewidth=1)
    
    plt.title(f'K-Line Chart: {stock_code} ({start_date} to {end_date})', fontsize=14)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price (¥)', fontsize=12)
    plt.grid(True, alpha=0.3)
    
    # Format x-axis
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
    plt.xticks(rotation=45)
    
    # Add price statistics
    stats_text = f"""
Price Statistics:
- Highest: ¥{df['high'].max():.2f}
- Lowest: ¥{df['low'].min():.2f}
- Average: ¥{df['close'].mean():.2f}
- Volatility: {df['close'].std():.2f}
"""
    plt.figtext(0.02, 0.02, stats_text, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
    
    plt.tight_layout()
    plt.show()
    
    # Print first and last few rows for verification
    print("\n[INFO] First 5 rows:")
    print(df.head().to_string(index=False))
    
    print("\n[INFO] Last 5 rows:")
    print(df.tail().to_string(index=False))

if __name__ == "__main__":
    fetch_and_plot_kline() 