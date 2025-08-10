#!/usr/bin/env python3
import sys
print("Python version:", sys.version)

try:
    import backtrader as bt
    print("✓ backtrader imported successfully")
except ImportError as e:
    print("✗ backtrader import failed:", e)

try:
    import pandas as pd
    print("✓ pandas imported successfully")
except ImportError as e:
    print("✗ pandas import failed:", e)

try:
    import baostock as bs
    print("✓ baostock imported successfully")
except ImportError as e:
    print("✗ baostock import failed:", e)

try:
    import matplotlib
    print("✓ matplotlib imported successfully")
except ImportError as e:
    print("✗ matplotlib import failed:", e)

print("Test completed!") 