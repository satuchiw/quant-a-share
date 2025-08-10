#!/usr/bin/env python3
"""
Simple test script to check Python environment and dependencies
"""

import sys
print(f"Python version: {sys.version}")

try:
    import pandas as pd
    print(f"Pandas version: {pd.__version__}")
except ImportError:
    print("Pandas not installed")

try:
    import backtrader as bt
    print(f"Backtrader version: {bt.__version__}")
except ImportError:
    print("Backtrader not installed")

try:
    import matplotlib
    print(f"Matplotlib version: {matplotlib.__version__}")
except ImportError:
    print("Matplotlib not installed")

print("Environment test completed")
