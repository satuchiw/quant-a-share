#!/usr/bin/env python3
import pandas as pd

def check_excel_data():
    """Check the structure of the Excel file"""
    excel_filename = "strategy_data_RSIStrategy_600600_2020-04-01_2025-04-01.xlsx"
    
    try:
        df = pd.read_excel(excel_filename)
        print(f"Excel file loaded successfully: {len(df)} rows")
        print(f"Columns: {list(df.columns)}")
        print(f"Data types: {df.dtypes}")
        print("\nFirst 5 rows:")
        print(df.head())
        print("\nLast 5 rows:")
        print(df.tail())
        
        # Check for any NaN values
        print(f"\nNaN values per column:")
        print(df.isnull().sum())
        
    except Exception as e:
        print(f"Error reading Excel file: {e}")

if __name__ == "__main__":
    check_excel_data() 