import pandas as pd

def clean_data(file_path):
    with open(file_path, 'r') as fil:
        file_content = fil.read()
        file_content = file_content.replace('Price', 'Date') #Replaces the 'Price' column with the 'Date'
    with open(file_path, 'w') as fil:
        fil.write(file_content)
    df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
    df.index = pd.to_datetime(df.index, errors='coerce').strftime('%Y-%m-%d') #gets rid of all the 00:00:00+00:00 in the date format
    df.dropna(inplace=True)  
    
    df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors='coerce') #Converts 'Adj Close' to numeric in case of errors
    df = df.dropna(subset=['Adj Close'])
    df['Daily Return'] = df['Adj Close'].pct_change() #calculates the daily returns for stock volatility examination
    
    return df

if __name__ == "__main__":
    cleaned_df = clean_data("data/stock_data.csv")
    print(cleaned_df.head())
    print(cleaned_df.columns)
    cleaned_df.to_csv("data/cleaned_stock_data.csv")
    print("Data cleaned and saved to data/cleaned_stock_data.csv")