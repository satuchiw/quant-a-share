#!/usr/bin/env python3
"""
Test script for performance analyzer
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from performance_analyzer import PerformanceAnalyzer

def test_performance_analyzer():
    """Test the performance analyzer with sample data"""
    
    print("Testing Performance Analyzer...")
    
    # Create sample portfolio values (simulating a strategy that starts with 100000 and grows)
    initial_value = 100000
    portfolio_values = []
    dates = []
    
    # Generate sample data for 1 year
    start_date = datetime(2020, 4, 1)
    for i in range(252):  # 252 trading days
        current_date = start_date + timedelta(days=i)
        # Simulate some growth with random fluctuations
        growth_rate = 0.0005 + np.random.normal(0, 0.02)  # 0.05% daily growth + noise
        if i == 0:
            current_value = initial_value
        else:
            current_value = portfolio_values[-1] * (1 + growth_rate)
        
        portfolio_values.append(current_value)
        dates.append(current_date)
    
    print(f"Generated {len(portfolio_values)} portfolio values")
    print(f"Portfolio range: {min(portfolio_values):.2f} to {max(portfolio_values):.2f}")
    
    # Create sample benchmark data
    benchmark_data = pd.DataFrame({
        'close': [100 + i * 0.1 + np.random.normal(0, 2) for i in range(len(dates))]
    }, index=dates)
    
    # Test the performance analyzer
    analyzer = PerformanceAnalyzer()
    
    # Test cumulative returns calculation
    cumulative_portfolio, cumulative_benchmark = analyzer.calculate_cumulative_returns(
        portfolio_values, benchmark_data
    )
    
    print(f"Cumulative portfolio returns: {len(cumulative_portfolio)} points")
    print(f"Cumulative benchmark returns: {len(cumulative_benchmark)} points")
    
    # Test plotting (without showing the plot)
    try:
        analyzer.plot_cumulative_returns(
            portfolio_values, dates, benchmark_data,
            "Test Strategy", "TEST.001"
        )
        print("✓ Plot function works correctly")
    except Exception as e:
        print(f"✗ Plot function failed: {e}")
    
    print("Performance analyzer test completed!")

if __name__ == "__main__":
    test_performance_analyzer() 