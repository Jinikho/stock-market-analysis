import pandas as pd
import itertools
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error

# Load the cleaned stock data
def load_data(file_path):
    df = pd.read_csv(file_path, index_col="Date", parse_dates=True)
    return df['Adj Close']

# Grid search to find optimal ARIMA parameters
def grid_search_arima(data, p_range, d_range, q_range):
    best_aic = float("inf")
    best_order = None
    best_model = None

    for p, d, q in itertools.product(p_range, d_range, q_range):
        try:
            model = ARIMA(data, order=(p, d, q))
            result = model.fit()
            if result.aic < best_aic:
                best_aic = result.aic
                best_order = (p, d, q)
                best_model = result
        except Exception as e:
            continue

    print(f"Best ARIMA Order: {best_order} with AIC: {best_aic}")
    return best_order, best_model

# Fit ARIMA model and forecast future values
def fit_arima_model(data, order, forecast_steps=30):
    model = ARIMA(data, order=order)
    result = model.fit()

    forecast = result.get_forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, freq='B')[1:]
    forecast_values = forecast.predicted_mean

    return result, forecast_index, forecast_values

if __name__ == "__main__":
    # Example standalone usage
    data = load_data("data/cleaned_stock_data.csv")
    
    # Define ranges for p, d, q
    p_range = range(0, 4)  # Adjust as needed
    d_range = range(0, 3)
    q_range = range(0, 4)

    # Perform grid search to find the best ARIMA parameters
    best_order, best_model = grid_search_arima(data, p_range, d_range, q_range)
    print(best_model.summary())

    # Forecast future values
    result, forecast_index, forecast_values = fit_arima_model(data, best_order)
    print("Forecast values:", forecast_values)