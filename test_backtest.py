#!/usr/bin/env python3
"""
Simple test script for the backtest system
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import backtrader
        print("✓ backtrader imported successfully")
    except ImportError as e:
        print(f"✗ backtrader import failed: {e}")
        return False
    
    try:
        import pandas
        print("✓ pandas imported successfully")
    except ImportError as e:
        print(f"✗ pandas import failed: {e}")
        return False
    
    try:
        import baostock
        print("✓ baostock imported successfully")
    except ImportError as e:
        print(f"✗ baostock import failed: {e}")
        return False
    
    try:
        import matplotlib
        print("✓ matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ matplotlib import failed: {e}")
        return False
    
    return True

def test_config_loading():
    """Test if configuration files can be loaded"""
    try:
        import json
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("✓ config.json loaded successfully")
        print(f"  Stock: {config.get('stock_code')}")
        print(f"  Strategy: {config.get('strategy')}")
        return True
    except Exception as e:
        print(f"✗ config.json loading failed: {e}")
        return False

def test_modules():
    """Test if our custom modules can be imported"""
    try:
        from data_fetcher import DataFetcher
        print("✓ data_fetcher imported successfully")
    except ImportError as e:
        print(f"✗ data_fetcher import failed: {e}")
        return False
    
    try:
        from strategies import STRATEGIES
        print("✓ strategies imported successfully")
        print(f"  Available strategies: {list(STRATEGIES.keys())}")
    except ImportError as e:
        print(f"✗ strategies import failed: {e}")
        return False
    
    try:
        from performance_analyzer import PerformanceAnalyzer
        print("✓ performance_analyzer imported successfully")
    except ImportError as e:
        print(f"✗ performance_analyzer import failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("="*50)
    print("BACKTEST SYSTEM TEST")
    print("="*50)
    
    # Test imports
    print("\n1. Testing imports...")
    if not test_imports():
        print("Import tests failed!")
        return
    
    # Test configuration
    print("\n2. Testing configuration...")
    if not test_config_loading():
        print("Configuration test failed!")
        return
    
    # Test modules
    print("\n3. Testing custom modules...")
    if not test_modules():
        print("Module tests failed!")
        return
    
    print("\n" + "="*50)
    print("ALL TESTS PASSED!")
    print("="*50)
    print("\nYou can now run: python backtest.py config.json")

if __name__ == "__main__":
    main() 