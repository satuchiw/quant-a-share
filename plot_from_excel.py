#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt

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
    
    # Check which cumulative return columns exist
    strategy_cumulative_col = 'Cumulative_Return_x' if 'Cumulative_Return_x' in df.columns else 'Cumulative_Return'
    benchmark_cumulative_col = 'Cumulative_Return_y' if 'Cumulative_Return_y' in df.columns else 'CSI300_Cumulative_Return'
    
    if strategy_cumulative_col in df.columns:
        print(f"[INFO] Strategy cumulative return range: {df[strategy_cumulative_col].min():.4f} to {df[strategy_cumulative_col].max():.4f}")
    
    # Create the plot
    plt.figure(figsize=(14, 8))
    
    # Plot strategy cumulative returns
    if strategy_cumulative_col in df.columns:
        plt.plot(df['Date'], df[strategy_cumulative_col], 
                label='Strategy (RSI)', linewidth=2, color='blue')
    
    # Plot CSI300 cumulative returns if available
    if benchmark_cumulative_col in df.columns:
        plt.plot(df['Date'], df[benchmark_cumulative_col], 
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
    if strategy_cumulative_col in df.columns:
        final_strategy_return = (df[strategy_cumulative_col].iloc[-1] - 1) * 100
        plt.text(0.02, 0.98, f'Final Strategy Return: {final_strategy_return:.2f}%', 
                transform=plt.gca().transAxes, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightblue", alpha=0.8))
    
    if benchmark_cumulative_col in df.columns:
        final_benchmark_return = (df[benchmark_cumulative_col].iloc[-1] - 1) * 100
        plt.text(0.02, 0.92, f'Final CSI300 Return: {final_benchmark_return:.2f}%', 
                transform=plt.gca().transAxes, fontsize=10,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="lightcoral", alpha=0.8))
        
        # Calculate outperformance
        if strategy_cumulative_col in df.columns:
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
    
    if strategy_cumulative_col in df.columns:
        print(f"Final Strategy Return: {final_strategy_return:.2f}%")
    
    if benchmark_cumulative_col in df.columns:
        print(f"Final CSI300 Return: {final_benchmark_return:.2f}%")
        if strategy_cumulative_col in df.columns:
            print(f"Outperformance: {outperformance:+.2f}%")
    
    print("="*60)
    
    # Show sample data
    print("\nSample data from Excel:")
    print(df.head(10))
    print("\nLast 5 rows:")
    print(df.tail())

if __name__ == "__main__":
    excel_filename = "strategy_data_RSIStrategy_600600_2020-04-01_2025-04-01.xlsx"
    plot_from_excel(excel_filename) 