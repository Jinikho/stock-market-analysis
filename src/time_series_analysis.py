import pandas as pd
import itertools
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller

# Check stationarity using Augmented Dickey-Fuller test
def check_stationarity(data):
    print("Testing for stationarity...")
    result = adfuller(data)
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    if result[1] > 0.05:
        print("Data is not stationary. Consider differencing.")
        return False
    else:
        print("Data is stationary.")
        return True

# Load cleaned stock data with proper handling of missing or infinite values
def load_data(file_path):
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
    df.index = pd.to_datetime(df.index)  # Ensure DateTime index
    df = df.asfreq('B')  # Set frequency to business days

    # Handle missing or infinite values
    df['Adj Close'] = df['Adj Close'].ffill().bfill()  # Forward and backward fill
    df['Adj Close'] = df['Adj Close'].replace([float('inf'), float('-inf')], pd.NA).ffill().bfill()

    return df['Adj Close']

# Grid search to find optimal ARIMA parameters
def grid_search_arima(data, p_range, d_range, q_range):
    best_aic = float("inf")
    best_order = None
    best_model = None

    for p, d, q in itertools.product(p_range, d_range, q_range):
        try:
            model = ARIMA(data, order=(p, d, q), enforce_stationarity=False, enforce_invertibility=False)
            result = model.fit(method_kwargs={"maxiter": 1000})
            if result.aic < best_aic:
                best_aic = result.aic
                best_order = (p, d, q)
                best_model = result
        except Exception as e:
            print(f"Skipping ARIMA({p},{d},{q}) due to error: {e}")
            continue

    print(f"Best ARIMA Order: {best_order} with AIC: {best_aic}")
    return best_order, best_model

# Fit ARIMA model and forecast future values
def fit_arima_model(data, order, forecast_steps=30):
    if order is None:
        raise ValueError("No valid ARIMA model found. Please check your data or parameter ranges.")
    
    model = ARIMA(data, order=order, enforce_stationarity=False, enforce_invertibility=False)
    result = model.fit(method_kwargs={"maxiter": 1000})

    # Forecast future steps
    forecast = result.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, freq='B')[1:]
    forecast_values = forecast.predicted_mean

    return result, forecast_index, forecast_values

if __name__ == "__main__":
    # Load your cleaned stock data
    data = load_data("data/cleaned_stock_data.csv")

    # Check for stationarity
    is_stationary = check_stationarity(data)

    # If data is not stationary, apply differencing
    if not is_stationary:
        data = data.diff().dropna()  # First-order differencing
        print("Applied differencing. Retesting for stationarity...")
        check_stationarity(data)

    # Define parameter ranges for grid search
    p_range = range(0, 4)  # AR terms
    d_range = range(0, 3)  # Differencing terms
    q_range = range(0, 4)  # MA terms

    # Perform grid search to find the best ARIMA parameters
    best_order, best_model = grid_search_arima(data, p_range, d_range, q_range)
    if best_model:
        print(best_model.summary())

    # Forecast future values using the best ARIMA model
    try:
        result, forecast_index, forecast_values = fit_arima_model(data, best_order)

        # Transform forecast back to the original scale
        last_actual_price = load_data("data/cleaned_stock_data.csv").iloc[-1]  # Get the last actual price before differencing
        forecast_original_scale = forecast_values.cumsum() + last_actual_price

        # Create forecast DataFrame
        forecast_df = pd.DataFrame({
            'Date': forecast_index,
            'Forecast_Change': forecast_values,
            'Forecast_Original_Scale': forecast_original_scale
        })

        print("Forecast values:")
        print(forecast_df)
    except ValueError as e:
        print(e)