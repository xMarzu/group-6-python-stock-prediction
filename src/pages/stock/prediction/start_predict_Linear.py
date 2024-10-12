from linearRegression import download_data, preprocess_data, split_data, train_model, predict_next_day_price, validate_dates
from prophetModel import get_stock_data, fit_prophet_model, make_prediction, evaluate_prophet_model
from sklearn.metrics import r2_score
from dash import html, dcc, callback, Output, Input, State,dash_table
import numpy as np
import plotly.graph_objs as go

def start_predict_Linear(stock_id,prediction_date_start_linear,prediction_date_end_linear):
    invalid=[]
    invalid2=[]
    prophet_score=[]
    prophet_table=[]
    # Main Execution - Download stock data
    ticker = stock_id 
    start_date = prediction_date_start_linear
    end_date = prediction_date_end_linear
    stock_data, dates = download_data(ticker, start_date, end_date)

    # Preprocess data - Creates sequences of 10 days of stock prices, target on the 11th day
    sequence_length = 10
    data_sequences = preprocess_data(stock_data,dates, sequence_length)

    # Split data into training and testing sets
    train_data, test_data = split_data(data_sequences)

    # Prepare training data
    X_train = np.array([item[0] for item in train_data])
    y_train = np.array([item[1] for item in train_data])

    # Prepare testing data
    X_test = np.array([item[0] for item in test_data])
    y_test = np.array([item[1] for item in test_data])
    
    # Train linear regression model
    model = train_model(X_train, y_train)

    # Predict values for the test set
    y_pred = model.predict(X_test)

    # Prepare data for the graph
    actual_prices = [item[1] for item in test_data]
    prediction_dates = [item[2] for item in test_data]

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prediction_dates, y=actual_prices, mode='lines', name='Actual Prices'))
    fig.add_trace(go.Scatter(x=prediction_dates, y=y_pred, mode='lines', name='Predicted Prices'))

    
    
    # Predict the next day's stock price using the last available sequence
    last_sequence = stock_data.iloc[-sequence_length:].values  # Last 10 days before the last available date
    last_date = dates[-1]  # The last date in the dataset

    # Debug prints
    print(f"\nData Sequence used for prediction: {last_sequence}")
    print(f"Last date in the dataset: {last_date}")

    # Predict stock price for the next day
    predicted_price, next_day = predict_next_day_price(model, last_sequence, last_date)

    fig.add_trace(go.Scatter(x=[next_day], y=[predicted_price], mode='markers', name='Predicted Next Day', marker=dict(size=10, color='red')
    ))

    # Optionally, calculate R-squared score on the test set
    testing_x = np.array([item[0] for item in test_data])
    testing_y = np.array([item[1] for item in test_data])
    y_pred = model.predict(testing_x)
    r2 = r2_score(testing_y, y_pred)
    #First line is the next s
    r2_scores = f"\n**Predicted Stock Price for the next possible trading day**: ${predicted_price:.2f} \n\n"
    r2_scores2= f"**R-squared score:** {r2:.4f}  \n" \
                f"**Explanation:** The R-squared (R²) score measures how well the model predicts stock prices.  \n" \
                f"An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate."

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Linear Regression',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)
    return fig ,r2_scores,r2_scores2,invalid,prophet_score,prophet_score,invalid2,prophet_table