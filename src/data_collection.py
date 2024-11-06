import pandas as pd
import requests
import yfinance as yf



def fetch_stock_data(symbol, start_date=None, end_date=None):
    # Use specified dates or set defaults if None provided
    if start_date is None:
        start_date = "2020-01-01"  # default start date if not provided
    if end_date is None:
        end_date = pd.Timestamp.today().strftime("%Y-%m-%d")  # today's date as default end

    # Fetch data from Yahoo Finance
    stock_data = yf.download(symbol, start=start_date, end=end_date)
    return stock_data

if __name__ == "__main__":
    # Prompt the user to enter the start and end dates
    symbol = input("Enter the stock symbol (e.g., AAPL): ")
    start_date = input("Enter start date (YYYY-MM-DD) or leave blank for default: ") or None
    end_date = input("Enter end date (YYYY-MM-DD) or leave blank for default: ") or None
    
    # Fetch the data
    df = fetch_stock_data(symbol, start_date, end_date)
    print(df.head())
    df.to_csv("data/stock_data.csv")
    print("Data saved to data/stock_data.csv")