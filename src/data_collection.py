import pandas as pd
import yfinance as yf



def fetch_stock_data(symbol, start_date=None, end_date=None):
    # Specificed dates or default if None is provided
    if start_date is None:
        start_date = "2020-01-01"  # default start date if not provided
    if end_date is None:
        end_date = pd.Timestamp.today().strftime("%Y-%m-%d")  # today's date as default if None is provided

    # Fetching data from Yahoo Finance
    try:
        stock_data = yf.download(symbol, start=start_date, end=end_date)
        if stock_data.empty:
            raise ValueError(f"No data found for the ticker symbol '{symbol}'")
        return stock_data
    except Exception as e:
        print(f"Error fetching stock data: {symbol}: {e}")
        return None

if __name__ == "__main__":
    # User enters stock symbol, start and end dates
    symbol = input("Enter the stock symbol (e.g., AAPL): ")
    start_date = input("Enter start date (YYYY-MM-DD) or leave blank for default: ") or None
    end_date = input("Enter end date (YYYY-MM-DD) or leave blank for default: ") or None
    
    # Fetch the data and save to csv file
    df = fetch_stock_data(symbol, start_date, end_date)
    if df is None or df.empty:
        print("No data found for the specified symbol. Please enter valid symbol.")
    else:
        print("Data fethced successfully!")
        print(df.head())
        df.to_csv("data/stock_data.csv")
        print("Data saved to data/stock_data.csv")