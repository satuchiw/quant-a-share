import baostock as bs
import pandas as pd
import os
from datetime import datetime

class DataFetcher:
    """
    Data fetcher class that downloads historical stock data using Baostock API
    """
    
    def __init__(self):
        self.logged_in = False
        
    def login(self):
        """Login to Baostock API"""
        if not self.logged_in:
            print("[INFO] Logging in to Baostock...")
            lg = bs.login()
            if lg.error_code != '0':
                print(f"[ERROR] Login failed: {lg.error_msg}")
                return False
            else:
                print("[INFO] Login successful.")
                self.logged_in = True
        return True
    
    def logout(self):
        """Logout from Baostock API"""
        if self.logged_in:
            print("[INFO] Logging out from Baostock...")
            bs.logout()
            self.logged_in = False
    
    def fetch_data(self, stock_code, start_date, end_date, frequency="d", adjustflag="2"):
        """
        Fetch historical K-line data from Baostock
        
        Args:
            stock_code (str): Stock code (e.g., 'sh.600600')
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format
            frequency (str): Data frequency ('d' for daily, 'w' for weekly, 'm' for monthly)
            adjustflag (str): Adjustment flag ('1' for forward, '2' for backward, '3' for none)
            
        Returns:
            pandas.DataFrame: Historical price data
        """
        if not self.login():
            return None
            
        print(f"[INFO] Querying historical K data for {stock_code} from {start_date} to {end_date}...")
        
        rs = bs.query_history_k_data_plus(
            stock_code,
            "date,code,open,high,low,close,volume",
            start_date=start_date, 
            end_date=end_date,
            frequency=frequency, 
            adjustflag=adjustflag
        )
        
        if rs.error_code != '0':
            print(f"[ERROR] Query failed: {rs.error_msg}")
            return None
        else:
            print("[INFO] Query successful. Processing data...")
        
        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        
        if not data_list:
            print("[WARNING] No data returned for the given query.")
            return None
        else:
            df = pd.DataFrame(data_list, columns=rs.fields)
            return df
    
    def save_data(self, df, stock_code, start_date, end_date, output_dir="data"):
        """
        Save data to CSV file
        
        Args:
            df (pandas.DataFrame): Data to save
            stock_code (str): Stock code
            start_date (str): Start date
            end_date (str): End date
            output_dir (str): Output directory
            
        Returns:
            str: Path to saved CSV file
        """
        if df is None or df.empty:
            print("[ERROR] No data to save.")
            return None
            
        # Create filename
        code_short = stock_code.split('.')[-1]  # Extract code without exchange prefix
        filename = f"{code_short}_{start_date}_{end_date}.csv"
        filepath = os.path.join(output_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        print(f"[INFO] Data saved to {filepath}")
        
        return filepath
    
    def fetch_and_save(self, stock_code, start_date, end_date, frequency="d", adjustflag="2", output_dir="data"):
        """
        Fetch data and save to CSV in one operation
        
        Args:
            stock_code (str): Stock code
            start_date (str): Start date
            end_date (str): End date
            frequency (str): Data frequency
            adjustflag (str): Adjustment flag
            output_dir (str): Output directory
            
        Returns:
            str: Path to saved CSV file
        """
        df = self.fetch_data(stock_code, start_date, end_date, frequency, adjustflag)
        if df is not None:
            return self.save_data(df, stock_code, start_date, end_date, output_dir)
        return None
    
    def load_data_from_csv(self, filepath):
        """
        Load data from CSV file and prepare for backtesting
        
        Args:
            filepath (str): Path to CSV file
            
        Returns:
            pandas.DataFrame: Prepared data for backtesting
        """
        try:
            df = pd.read_csv(filepath)
            print(f"[INFO] Loaded data from {filepath}")
            
            # Prepare data for backtesting
            df['date'] = pd.to_datetime(df['date'])
            df.set_index('date', inplace=True)
            
            # Convert numeric columns
            numeric_columns = ['open', 'high', 'low', 'close', 'volume']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            return df
            
        except FileNotFoundError:
            print(f"[ERROR] File not found: {filepath}")
            return None
        except Exception as e:
            print(f"[ERROR] Error loading data: {e}")
            return None


if __name__ == "__main__":
    # Example usage
    fetcher = DataFetcher()
    
    # Fetch data for 600600
    stock_code = "sh.600600"
    start_date = "2020-04-01"
    end_date = "2021-04-01"
    
    csv_path = fetcher.fetch_and_save(stock_code, start_date, end_date)
    
    if csv_path:
        # Load and prepare data
        df = fetcher.load_data_from_csv(csv_path)
        if df is not None:
            print(f"[INFO] Data shape: {df.shape}")
            print(f"[INFO] Date range: {df.index.min()} to {df.index.max()}")
    
    fetcher.logout() 