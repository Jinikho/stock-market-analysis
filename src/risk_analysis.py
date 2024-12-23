import pandas as pd
import numpy as np

def calculate_var(daily_returns, confidence_level=0.05):

    var = np.percentile(daily_returns.dropna(), 100 * confidence_level)
    return var

def calculate_sharpe_ratio(daily_returns, risk_free_rate=0):
   
    mean_return = daily_returns.mean()
    return_std = daily_returns.std()
    sharpe_ratio = (mean_return - risk_free_rate) / return_std
    return sharpe_ratio

if __name__ == "__main__":
    # Loading cleaned stock data
    df = pd.read_csv("data/cleaned_stock_data.csv", index_col="Date", parse_dates=True)

    #  risk metrics calculation
    daily_returns = df["Daily Return"]

    # Value at Risk (VaR) calc.
    var = calculate_var(daily_returns, confidence_level=0.05)
    print(f"5% Value at Risk (VaR): {var:.4f}")

    #  Sharpe Ratio calcul.
    risk_free_rate = 0  
    sharpe_ratio = calculate_sharpe_ratio(daily_returns, risk_free_rate)
    print(f"Sharpe Ratio: {sharpe_ratio:.2f}")