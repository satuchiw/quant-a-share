# Quantitative Trading Backtesting System

A comprehensive quantitative trading backtesting framework built with Python and Backtrader, designed for Chinese stock market analysis and strategy development.

## 🚀 Features

- **Multiple Trading Strategies**: RSI, Moving Average Crossover, Bollinger Bands
- **Comprehensive Backtesting**: Full OHLCV data support with realistic trading simulation
- **Performance Analytics**: Sharpe ratio, drawdown analysis, trade statistics
- **Data Management**: Automated data fetching and CSV processing
- **Visualization**: Interactive charts and performance plots
- **Configuration System**: JSON-based strategy parameter management

## 📁 Project Structure

```
quant-a-share/
├── backtest.py              # Main backtesting engine
├── strategies.py            # Trading strategy implementations
├── data_fetcher.py          # Data fetching and processing
├── performance_analyzer.py  # Performance analysis tools
├── config_*.json           # Strategy configuration files
├── *.csv                   # Stock data files
└── README.md              # This file
```

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <your-repo-url>
   cd quant-a-share
   ```

2. **Install dependencies**:
   ```bash
   pip install backtrader pandas matplotlib numpy
   ```

3. **Optional dependencies**:
   ```bash
   pip install jupyter notebook  # For Jupyter notebooks
   ```

## 📊 Available Strategies

### 1. RSI Strategy
- **Logic**: Buy when RSI < 30 (oversold), sell when RSI > 70 (overbought)
- **Parameters**: RSI period, oversold/overbought thresholds
- **Config**: `config_rsi.json`

### 2. Moving Average Crossover
- **Logic**: Buy when short MA crosses above long MA, sell on reverse
- **Parameters**: Short/long moving average periods
- **Config**: `config.json`

### 3. Bollinger Bands Strategy
- **Logic**: Buy when price touches lower band, sell when touching upper band
- **Parameters**: BB period, standard deviation multiplier
- **Config**: `config_bollinger.json`

## 🚀 Usage

### Basic Backtesting
```bash
python backtest.py config_rsi.json
```

### Custom Configuration
1. Edit the JSON config file with your parameters
2. Run the backtest with your config:
   ```bash
   python backtest.py your_config.json
   ```

### Configuration Parameters
```json
{
    "stock_code": "sh.603259",
    "start_date": "2022-02-01",
    "end_date": "2025-08-01",
    "strategy": "RSIStrategy",
    "initial_cash": 100000,
    "strategy_params": {
        "rsi_period": 14,
        "oversold": 30,
        "overbought": 70
    }
}
```

## 📈 Performance Metrics

The system provides comprehensive performance analysis:

- **Sharpe Ratio**: Risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Total Return**: Overall strategy performance
- **Trade Statistics**: Win/loss ratios, trade counts, streaks
- **Portfolio Tracking**: Daily portfolio value changes

## 📊 Data Sources

- **Stock Data**: Shanghai and Shenzhen market data
- **Format**: OHLCV (Open, High, Low, Close, Volume)
- **Frequency**: Daily data
- **Adjustment**: Price-adjusted for dividends and splits

## 🔧 Development

### Adding New Strategies
1. Create a new strategy class in `strategies.py`
2. Inherit from `bt.Strategy`
3. Implement the `next()` method with your logic
4. Add strategy parameters to the `params` tuple

### Example Strategy Template
```python
class MyStrategy(bt.Strategy):
    params = (
        ('param1', 10),
        ('param2', 20),
    )
    
    def __init__(self):
        # Initialize indicators
        pass
    
    def next(self):
        # Implement trading logic
        pass
```

## 📝 Configuration Files

- `config.json`: Default MA strategy configuration
- `config_rsi.json`: RSI strategy configuration
- `config_bollinger.json`: Bollinger Bands strategy configuration

## 🧪 Testing

Run the test suite:
```bash
python test_backtest.py
python test_performance.py
python test_portfolio_tracking.py
```

## 📊 Sample Results

The system generates detailed backtest reports including:
- Performance metrics summary
- Interactive charts with candlesticks and volume
- Cumulative returns comparison
- Trade analysis and statistics

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes only. Past performance does not guarantee future results. Always conduct thorough testing before using any trading strategy with real money.

## 📞 Support

For questions or issues, please open an issue on the GitHub repository.

---

**Note**: This is a quantitative trading research tool. Use at your own risk and always validate strategies thoroughly before live trading.
