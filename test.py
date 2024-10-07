import dash
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
from src.components.stock.single_stock_base_layout import stock_base_layout
from linearRegression import download_stock_data, preprocess_data, split_data, train_model
import numpy as np
from sklearn.metrics import r2_score
import pandas as pd

dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    return html.Div([
        stock_base_layout(stock_id),
        html.H3("Stock Price Prediction"),
        dcc.Input(id='days-to-predict', type='number', value=1, min=1, step=1),
        html.Button('Predict', id='predict-button', n_clicks=0),
        dcc.Graph(id='prediction-graph'),
    ])

def start_predict(stock_id, days_to_predict):
    # Main Execution - Download stock data
    ticker = "MMM"
    start_date = '2014-01-01'
    end_date = '2024-09-17'
    stock_data, dates = download_stock_data(ticker, start_date, end_date)

    # Preprocess data - Creates sequences of 10 days of stock prices, target on the 11th day
    sequence_length = 10
    data_sequences = preprocess_data(stock_data, dates, sequence_length)

    # Split data into training and testing sets
    train_data, test_data = split_data(data_sequences)

    # Prepare training data
    X_train = np.array([item[0] for item in train_data])
    y_train = np.array([item[1] for item in train_data])

    # Train linear regression model
    model = train_model(X_train, y_train)

    # Prepare the last sequence for future predictions
    last_sequence = stock_data[-sequence_length:].values.reshape(1, -1)

    # Predict future prices
    future_predictions = []
    for _ in range(days_to_predict):
        # Predict the next price
        next_price = model.predict(last_sequence)[0]
        future_predictions.append(next_price)

        # Update the last_sequence for the next prediction
        last_sequence = np.append(last_sequence[:, 1:], next_price).reshape(1, -1)

    # Prepare data for the graph
    actual_prices = [item[1] for item in test_data]
    prediction_dates = [item[2] for item in test_data]
    future_dates = pd.date_range(start=prediction_dates[-1] + pd.Timedelta(days=1), periods=days_to_predict)

    # Calculate R-squared score
    y_test = np.array([item[1] for item in test_data])
    y_pred = model.predict(np.array([item[0] for item in test_data]))
    r2 = r2_score(y_test, y_pred)

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prediction_dates, y=actual_prices, mode='lines', name='Actual Prices'))
    fig.add_trace(go.Scatter(x=future_dates, y=future_predictions, mode='lines+markers', name='Future Predictions'))

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker}',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)

    return fig

@callback(
    Output('prediction-graph', 'figure'),
    Input('url', 'pathname'),
    Input('predict-button', 'n_clicks'),
    Input('days-to-predict', 'value')
)
def update_graph(pathname, n_clicks, days_to_predict):
    stock_id = pathname.split('/')[-2]  # Extract stock_id from the URL
    if n_clicks > 0:
        return start_predict(stock_id, days_to_predict)
    return go.Figure()  # Return an empty figure initially
