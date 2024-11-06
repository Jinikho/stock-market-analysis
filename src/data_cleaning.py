import pandas as pd

def clean_data(file_path):
    
    data = pd.read_csv(file_path)
    
    #remove any missing values
    df = data.dropna().copy()
    
    df['Adj Close'] = pd.to_numeric(df['Adj Close'], errors=('coerce'))
    df = df.dropna(subset=['Adj Close'])
    #Reset indexes
    df = df.reset_index(drop=True)
    #Daily returns for volatility examination
    df['Daily Return'] = df['Adj Close'].pct_change()
    
    return df

if __name__ == "__main__":
    
    cleaned_df = clean_data("data/stock_data.csv")
    print(cleaned_df.head())
    cleaned_df.to_csv("data/cleaned_stock_data.csv")
    print("Data cleaned and saved to data/cleaned_stock_data.csv")