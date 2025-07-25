import baostock as bs
import pandas as pd

print("[INFO] Logging in to Baostock...")
lg = bs.login()
if lg.error_code != '0':
    print(f"[ERROR] Login failed: {lg.error_msg}")
    exit(1)
else:
    print("[INFO] Login successful.")

print("[INFO] Querying historical K data for sh.600600 from 2020-04-01 to 2021-04-01...")
rs = bs.query_history_k_data_plus(
    "sh.600600",
    "date,code,open,high,low,close,volume",
    start_date='2020-04-01', end_date='2021-04-01',
    frequency="d", adjustflag="2"
)
if rs.error_code != '0':
    print(f"[ERROR] Query failed: {rs.error_msg}")
    bs.logout()
    exit(1)
else:
    print("[INFO] Query successful. Processing data...")

data_list = []
while (rs.error_code == '0') & rs.next():
    data_list.append(rs.get_row_data())

if not data_list:
    print("[WARNING] No data returned for the given query.")
else:
    df = pd.DataFrame(data_list, columns=rs.fields)
    csv_path = "600600_SH_2020_2021.csv"
    df.to_csv(csv_path, index=False)
    print(f"[INFO] Data saved to {csv_path}")

    # Plot daily K-Line (candlestick chart)
    try:
        import mplfinance as mpf
    except ImportError:
        print("[ERROR] mplfinance is not installed. Please install it with 'pip install mplfinance'.")
    else:
        kline_df = df[['date', 'open', 'high', 'low', 'close', 'volume']].copy()
        kline_df['date'] = pd.to_datetime(kline_df['date'])
        kline_df.set_index('date', inplace=True)
        kline_df[['open', 'high', 'low', 'close', 'volume']] = kline_df[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric, errors='coerce')
        mpf.plot(kline_df, type='candle', volume=True, title='Daily K-Line (Candlestick) for sh.600600 (2020-04-01 to 2021-04-01)', style='charles')

print("[INFO] Logging out from Baostock...")
bs.logout()
print("[INFO] Script finished.") 