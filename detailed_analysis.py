#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def detailed_analysis():
    """
    Perform detailed analysis of the strategy performance
    """
    excel_filename = "strategy_data_RSIStrategy_600600_2020-04-01_2025-04-01.xlsx"
    
    # Read data from Excel
    df = pd.read_excel(excel_filename)
    df['Date'] = pd.to_datetime(df['Date'])
    
    print("="*60)
    print("DETAILED STRATEGY ANALYSIS")
    print("="*60)
    
    # Analyze portfolio value changes
    df['Portfolio_Change'] = df['Portfolio_Value'].diff()
    significant_changes = df[abs(df['Portfolio_Change']) > 1]
    
    print(f"Total days: {len(df)}")
    print(f"Days with significant portfolio changes (>¥1): {len(significant_changes)}")
    print(f"Portfolio value range: ¥{df['Portfolio_Value'].min():.2f} to ¥{df['Portfolio_Value'].max():.2f}")
    print(f"Total portfolio change: ¥{df['Portfolio_Value'].iloc[-1] - df['Portfolio_Value'].iloc[0]:.2f}")
    
    # Show significant changes
    if len(significant_changes) > 0:
        print(f"\nSignificant portfolio changes:")
        for idx, row in significant_changes.iterrows():
            print(f"  {row['Date'].strftime('%Y-%m-%d')}: ¥{row['Portfolio_Change']:+.2f}")
    
    # Create a more detailed plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12))
    
    # Plot 1: Portfolio Value Over Time
    ax1.plot(df['Date'], df['Portfolio_Value'], linewidth=2, color='blue', label='Portfolio Value')
    ax1.set_title('Portfolio Value Over Time', fontsize=14, fontweight='bold')
    ax1.set_ylabel('Portfolio Value (¥)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Add horizontal line for initial value
    initial_value = df['Portfolio_Value'].iloc[0]
    ax1.axhline(y=initial_value, color='red', linestyle='--', alpha=0.7, label=f'Initial Value (¥{initial_value:,.0f})')
    ax1.legend()
    
    # Plot 2: Cumulative Returns Comparison
    strategy_cumulative_col = 'Cumulative_Return_x' if 'Cumulative_Return_x' in df.columns else 'Cumulative_Return'
    benchmark_cumulative_col = 'Cumulative_Return_y' if 'Cumulative_Return_y' in df.columns else 'CSI300_Cumulative_Return'
    
    if strategy_cumulative_col in df.columns:
        ax2.plot(df['Date'], df[strategy_cumulative_col], 
                label='Strategy (RSI)', linewidth=2, color='blue')
    
    if benchmark_cumulative_col in df.columns:
        ax2.plot(df['Date'], df[benchmark_cumulative_col], 
                label='CSI300 Index', linewidth=2, color='red', linestyle='--')
    
    ax2.set_title('Cumulative Returns Comparison', fontsize=14, fontweight='bold')
    ax2.set_xlabel('Date', fontsize=12)
    ax2.set_ylabel('Cumulative Return (Base = 100%)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Format x-axis
    for ax in [ax1, ax2]:
        ax.xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y-%m-%d'))
        ax.xaxis.set_major_locator(plt.matplotlib.dates.MonthLocator(interval=6))
        ax.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    # Calculate and display performance metrics
    print(f"\nPERFORMANCE METRICS:")
    print(f"="*40)
    
    if strategy_cumulative_col in df.columns:
        final_strategy_return = (df[strategy_cumulative_col].iloc[-1] - 1) * 100
        print(f"Strategy Final Return: {final_strategy_return:.2f}%")
    
    if benchmark_cumulative_col in df.columns:
        final_benchmark_return = (df[benchmark_cumulative_col].iloc[-1] - 1) * 100
        print(f"CSI300 Final Return: {final_benchmark_return:.2f}%")
        
        if strategy_cumulative_col in df.columns:
            outperformance = final_strategy_return - final_benchmark_return
            print(f"Outperformance: {outperformance:+.2f}%")
    
    # Calculate volatility
    if strategy_cumulative_col in df.columns:
        strategy_returns = df[strategy_cumulative_col].pct_change().dropna()
        strategy_volatility = strategy_returns.std() * np.sqrt(252) * 100
        print(f"Strategy Volatility: {strategy_volatility:.2f}%")
    
    if benchmark_cumulative_col in df.columns:
        benchmark_returns = df[benchmark_cumulative_col].pct_change().dropna()
        benchmark_volatility = benchmark_returns.std() * np.sqrt(252) * 100
        print(f"CSI300 Volatility: {benchmark_volatility:.2f}%")
    
    # Show the actual trades from the backtest log
    print(f"\nACTUAL TRADES EXECUTED:")
    print(f"="*40)
    trades = [
        ("2021-03-01", "BUY", 72.53),
        ("2021-04-22", "SELL", 84.24),
        ("2021-08-02", "BUY", 71.64),
        ("2021-11-01", "SELL", 95.09),
        ("2022-03-30", "BUY", 70.25),
        ("2022-06-28", "SELL", 90.37),
        ("2022-10-28", "BUY", 79.57),
        ("2023-04-11", "SELL", 113.12),
        ("2023-05-31", "BUY", 90.35),
        ("2024-02-26", "SELL", 78.12),
        ("2024-05-31", "BUY", 72.92),
        ("2024-09-30", "SELL", 72.69),
        ("2025-02-06", "BUY", 65.43)
    ]
    
    for date, action, price in trades:
        print(f"  {date}: {action} at ¥{price:.2f}")
    
    # Calculate trade returns
    print(f"\nTRADE ANALYSIS:")
    print(f"="*40)
    trade_returns = []
    for i in range(0, len(trades)-1, 2):
        if i+1 < len(trades):
            buy_price = trades[i][2]
            sell_price = trades[i+1][2]
            trade_return = (sell_price - buy_price) / buy_price * 100
            trade_returns.append(trade_return)
            print(f"  Trade {i//2 + 1}: Buy ¥{buy_price:.2f} → Sell ¥{sell_price:.2f} = {trade_return:+.2f}%")
    
    if trade_returns:
        print(f"\nTrade Statistics:")
        print(f"  Average trade return: {np.mean(trade_returns):.2f}%")
        print(f"  Best trade: {max(trade_returns):.2f}%")
        print(f"  Worst trade: {min(trade_returns):.2f}%")
        print(f"  Winning trades: {sum(1 for r in trade_returns if r > 0)}/{len(trade_returns)}")

if __name__ == "__main__":
    detailed_analysis() 