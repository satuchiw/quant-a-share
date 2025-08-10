#!/usr/bin/env python3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from performance_analyzer import PerformanceAnalyzer

def test_cumulative_returns():
    """Test cumulative returns calculation with significant changes"""
    
    # Create portfolio values with significant changes
    initial_value = 100000
    portfolio_values = [initial_value]
    
    # Simulate 30 days with realistic changes
    for i in range(1, 31):
        # Simulate daily changes (-2% to +2%)
        daily_change_pct = np.random.normal(0.001, 0.02)  # 0.1% mean, 2% std
        daily_change = portfolio_values[-1] * daily_change_pct
        new_value = portfolio_values[-1] + daily_change
        portfolio_values.append(new_value)
    
    print(f"Portfolio values: {len(portfolio_values)} points")
    print(f"Portfolio range: {min(portfolio_values):.2f} to {max(portfolio_values):.2f}")
    
    # Test the performance analyzer
    analyzer = PerformanceAnalyzer()
    
    # Calculate cumulative returns
    cumulative_portfolio, cumulative_benchmark = analyzer.calculate_cumulative_returns(
        portfolio_values, None
    )
    
    print(f"\nCumulative returns: {len(cumulative_portfolio)} points")
    print(f"Cumulative range: {min(cumulative_portfolio):.4f} to {max(cumulative_portfolio):.4f}")
    print(f"Final return: {(cumulative_portfolio[-1] - 1) * 100:.2f}%")
    
    # Create dates for plotting
    dates = pd.date_range('2020-01-01', periods=len(portfolio_values), freq='D')
    
    # Test plotting
    try:
        analyzer.plot_cumulative_returns(
            portfolio_values, dates, None,
            "Test Strategy", "TEST.001"
        )
        print("✓ Plot function works correctly")
    except Exception as e:
        print(f"✗ Plot function failed: {e}")

if __name__ == "__main__":
    test_cumulative_returns() 