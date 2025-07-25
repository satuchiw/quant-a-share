# Quantitative Trading Project

This repository contains code and data for quantitative trading research and backtesting. It is designed to help you analyze, develop, and test trading strategies using Python and popular data science libraries.

## Project Structure

```
quant/
├── anaconda_projects/           # Anaconda project files and database
├── data/                        # Data files (CSV format)
├── backtest.py                  # Main backtesting script (Backtrader-based)
├── strategy.py                  # Trading strategy definitions
├── readdata.py                  # Data loading and preprocessing
├── *.ipynb                      # Jupyter notebooks for exploration and analysis
├── PythonApplication1/          # Visual Studio Python project (optional)
```

## Key Files

- **backtest.py**: Main script for running backtests using Backtrader. Includes data import, backtest execution, and result analysis functions.
- **strategy.py**: Contains trading strategy logic (e.g., moving average crossover).
- **readdata.py**: Utilities for reading and preparing data from CSV files.
- **data/**: Folder containing historical price and profit data in CSV format.
- **.ipynb files**: Jupyter notebooks for interactive analysis, prototyping, and visualization.

## Getting Started

1. **Install Dependencies**
   - Recommended: Use [Anaconda](https://www.anaconda.com/) for environment management.
   - Required Python packages: `pandas`, `numpy`, `matplotlib`, `backtrader`.
   - Install with pip:
     ```bash
     pip install pandas numpy matplotlib backtrader
     ```

2. **Prepare Data**
   - Place your historical data CSV files in the `data/` directory.
   - Example files: `002415_day_kline_info.csv`, `002415_profit_info.csv`.

3. **Run Backtest**
   - Edit `backtest.py` to specify your strategy and data file.
   - Run the script:
     ```bash
     python backtest.py
     ```

4. **Explore Notebooks**
   - Use JupyterLab or Jupyter Notebook to open and run the `.ipynb` files for interactive analysis.

## Features

- Modular code for data loading, strategy definition, and backtesting
- Example moving average crossover strategy (commented in `backtest.py`)
- Performance analysis: trade statistics, drawdown, Sharpe ratio, annual returns
- Data visualization with Matplotlib

## Customization

- Add or modify strategies in `strategy.py` or directly in `backtest.py`.
- Use your own data by placing CSV files in the `data/` folder and updating file paths.
- Extend analysis and visualization in the provided notebooks.

## License

This project is for educational and research purposes. Please check data source licenses before using for commercial purposes.

---

Feel free to ask for help or request new features! 