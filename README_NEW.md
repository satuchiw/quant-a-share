# Quantitative Trading Backtesting System

This is a modular quantitative trading backtesting system designed for Chinese A-share markets. The system uses configuration files to define backtest parameters and supports multiple trading strategies.

## Features

- **Modular Design**: Separate files for strategies, data fetching, and backtesting
- **Configuration-Driven**: Use JSON files to define backtest parameters
- **Multiple Strategies**: Moving Average, RSI, Bollinger Bands strategies included
- **Automatic Data Download**: Downloads historical data from Baostock API
- **Comprehensive Analytics**: Sharpe ratio, drawdown, returns, trade statistics
- **Visualization**: Automatic plotting of backtest results

## File Structure

```
quant-a-share/
├── backtest.py              # Main backtesting engine
├── strategies.py            # Trading strategies
├── data_fetcher.py          # Data download and management
├── config.json              # Default configuration
├── config_rsi.json          # RSI strategy configuration
├── config_bollinger.json    # Bollinger Bands configuration
├── README_NEW.md           # This file
└── data/                   # Data storage directory
```

## Quick Start

### 1. Install Dependencies

```bash
pip install backtrader pandas baostock matplotlib mplfinance
```

### 2. Run Default Backtest

```bash
python backtest.py
```

This will use the default configuration in `config.json` to run a Moving Average strategy on stock 600600.

### 3. Use Different Strategies

To test different strategies, modify the configuration file or use a different one:

```bash
# For RSI strategy
python backtest.py config_rsi.json

# For Bollinger Bands strategy  
python backtest.py config_bollinger.json
```

## Configuration Files

Configuration files are in JSON format and contain:

```json
{
    "stock_code": "sh.600600",           // Stock code with exchange prefix
    "start_date": "2020-04-01",         // Start date (YYYY-MM-DD)
    "end_date": "2021-04-01",           // End date (YYYY-MM-DD)
    "strategy": "MAStrategy",            // Strategy name
    "initial_cash": 100000,              // Starting capital
    "strategy_params": {                 // Strategy-specific parameters
        "short_window": 10,
        "long_window": 30
    },
    "data_frequency": "d",               // Data frequency (d/w/m)
    "adjustflag": "2"                    // Price adjustment (1/2/3)
}
```

## Available Strategies

### 1. MAStrategy (Moving Average Crossover)
- **Logic**: Buy when short MA crosses above long MA, sell when it crosses below
- **Parameters**: `short_window`, `long_window`
- **Best for**: Trend-following strategies

### 2. RSIStrategy (Relative Strength Index)
- **Logic**: Buy when RSI < oversold threshold, sell when RSI > overbought threshold
- **Parameters**: `rsi_period`, `oversold`, `overbought`
- **Best for**: Mean reversion strategies

### 3. BollingerBandsStrategy
- **Logic**: Buy when price touches lower band, sell when price touches upper band
- **Parameters**: `bb_period`, `bb_dev`
- **Best for**: Volatility-based strategies

## Data Management

The system automatically:
1. Checks if data file exists locally
2. Downloads data from Baostock if not found
3. Saves data to CSV for future use
4. Prepares data for backtesting

Data files are named: `{stock_code}_{start_date}_{end_date}.csv`

## Performance Metrics

The system calculates:
- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Total Return**: Overall performance
- **Annual Return**: Yearly performance
- **Trade Statistics**: Win/loss ratio, streaks
- **Final Portfolio Value**: Ending capital

## Customization

### Adding New Strategies

1. Create a new strategy class in `strategies.py`:
```python
class MyStrategy(bt.Strategy):
    params = (('param1', 10), ('param2', 20))
    
    def __init__(self):
        # Initialize indicators
        pass
        
    def next(self):
        # Implement trading logic
        pass
```

2. Add to the STRATEGIES dictionary:
```python
STRATEGIES = {
    'MyStrategy': MyStrategy,
    # ... existing strategies
}
```

3. Create a configuration file for your strategy.

### Modifying Data Sources

Edit `data_fetcher.py` to use different data sources or add new data processing methods.

## Example Usage

### Basic Usage
```bash
# Run with default configuration
python backtest.py

# Run with specific configuration
python backtest.py my_config.json
```

### Configuration Examples

**Moving Average Strategy:**
```json
{
    "stock_code": "sh.600600",
    "start_date": "2020-01-01",
    "end_date": "2021-12-31",
    "strategy": "MAStrategy",
    "strategy_params": {
        "short_window": 5,
        "long_window": 20
    }
}
```

**RSI Strategy:**
```json
{
    "stock_code": "sz.000001",
    "start_date": "2020-01-01", 
    "end_date": "2021-12-31",
    "strategy": "RSIStrategy",
    "strategy_params": {
        "rsi_period": 14,
        "oversold": 25,
        "overbought": 75
    }
}
```

## Troubleshooting

### Common Issues

1. **Baostock Login Failed**: Check internet connection and Baostock service status
2. **No Data Downloaded**: Verify stock code format (e.g., "sh.600600" not "600600")
3. **Strategy Not Found**: Check strategy name in configuration matches STRATEGIES dictionary
4. **Plot Not Generated**: Install matplotlib and ensure display is available

### Data Format

Stock codes should include exchange prefix:
- Shanghai: `sh.600600`
- Shenzhen: `sz.000001`
- Beijing: `bj.430047`

## License

This project is for educational and research purposes. Please check data source licenses before commercial use. 