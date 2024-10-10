import pandas as pd
import yfinance as yf
from prophet import Prophet
from datetime import datetime, timedelta
from prophet.diagnostics import cross_validation, performance_metrics

def get_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()  # Reset the index to get 'Date' as a column
    data = data[['Date', 'Adj Close']]  # Use 'Date' and 'Adj Close' for prediction
    data.columns = ['ds', 'y']  # Rename columns to match Prophet's expected format
    data['ds'] = pd.to_datetime(data['ds']).dt.date  # Ensure 'ds' column is in date format
    return data

def fit_prophet_model(stock_data):
    """
    Fit the Prophet model to the historical stock data.
    """
    model = Prophet()
    model.fit(stock_data)
    return model

def make_prediction(model, stock_data, end_date, predict_date):
    """
    Make a prediction for the specified date using the fitted Prophet model.
    """
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S").date()
    predict_date_dt = datetime.strptime(predict_date, "%Y-%m-%d %H:%M:%S").date()
    
    print(f"End date: {end_date_dt}")
    print(f"Prediction date: {predict_date_dt}")
    
# If the prediction date is within the historical data range
    if stock_data['ds'].min() <= predict_date_dt <= stock_data['ds'].max():
        print(f"{predict_date_dt} is within the historical data range.")
        
        # Check if the prediction date is in the historical data (i.e., a trading day)
        if predict_date_dt not in stock_data['ds'].values:
            print(f"Error: {predict_date} is not a trading day. No historic data available.")
            return None, None
        
        # Make a prediction using the Prophet model
        future = model.make_future_dataframe(periods=0)  # No need to extend the future dataframe
        # print(f"Future dataframe for historical prediction:\n{future.tail()}")  #Print the future dataframe
        forecast = model.predict(future)
        # print(f"Forecast dataframe for historical prediction:\n{forecast.tail()}")  #Print the forecast dataframe
        
        # Retrieve the actual historical price for comparison
        actual_price = stock_data[stock_data['ds'] == predict_date_dt]['y'].values[0]
        predicted_price = forecast[forecast['ds'] == predict_date]['yhat'].values[0]
        
        print(f"Actual price for {predict_date}: {actual_price}")
        print(f"Predicted price for {predict_date}: {predicted_price}")
        return predicted_price, actual_price
    
    # If the prediction date is beyond the end date, proceed with future prediction
    else:
        print(f"{predict_date_dt} is beyond the historical data range.")
        
        # Create future dataframe to predict up to the specified prediction date
        future = model.make_future_dataframe(periods=0, freq='D')
        
        # Convert predict_date_dt to datetime64[ns] for comparison
        predict_date_dt = pd.to_datetime(predict_date_dt)
        
        # Ensure the future dataframe includes the prediction date
        last_date = future['ds'].max()
        additional_dates = []
        while last_date < predict_date_dt:
            last_date += timedelta(days=1)
            additional_dates.append({'ds': last_date})
            print(f"Adding date: {last_date}")  #Print each date being added
        
        if additional_dates:
            future = pd.concat([future, pd.DataFrame(additional_dates)], ignore_index=True)
        
        print(f"Extended future dataframe:\n{future.tail()}")  #Print the extended future dataframe
        
        forecast = model.predict(future)
        print(f"Forecast dataframe:\n{forecast.tail()}")  #Print the forecast dataframe
        
        # Output the prediction for the specified date
        prediction = forecast[forecast['ds'] == predict_date_dt]
        print(f"Prediction dataframe for {predict_date_dt}:\n{prediction}")
        
        if not prediction.empty:
            predicted_price = prediction['yhat'].values[0]
            print(f"Predicted price for {predict_date}: {predicted_price}")
            return predicted_price, None
        else:
            print(f"No prediction available for {predict_date}.")
            return None, None

def evaluate_prophet_model(stock_data, initial='365 days', period='180 days', horizon='365 days'):
    """
    Evaluate the Prophet model using cross-validation and performance metrics.
    
    Parameters:
    - stock_data: DataFrame containing the historical stock data.
    - initial: The size of the initial training period.
    - period: The spacing between cutoff dates.
    - horizon: The forecast horizon.
    
    Returns:
    - metrics: DataFrame containing the performance metrics.
    """
    # Fit the Prophet model
    model = fit_prophet_model(stock_data)
    
    # Perform cross-validation
    df_cv = cross_validation(model, initial=initial, period=period, horizon=horizon)
    
    # Calculate performance metrics
    df_metrics = performance_metrics(df_cv)
    return df_metrics

def main():
    # Input parameters
    ticker = input("Enter the stock symbol: ")
    start_date = input("Enter the start date (YYYY-MM-DD): ")
    end_date = input("Enter the end date (YYYY-MM-DD): ")
    predict_date = input("Enter the date to predict (YYYY-MM-DD): ")
    
    stock_data = get_stock_data(ticker, start_date, end_date)
    model = fit_prophet_model(stock_data)
    predicted_price, actual_price = make_prediction(model, stock_data, end_date, predict_date)
    
    if predicted_price is not None:
        if actual_price is not None:
            print("-"*100)
            print(f"The predicted price for {predict_date} is {predicted_price}, and the actual price was {actual_price}.")
        else:
            print("-"*100)
            print(f"The predicted price for {predict_date} is {predicted_price}.")
    else:
        print("-"*100)
        print("Prediction could not be made.")
    
    # Evaluate the model using evaluate_prophet_model func().
    metrics = evaluate_prophet_model(stock_data)
    print("Model performance metrics:")
    print(metrics)

if __name__ == "__main__":
    main()