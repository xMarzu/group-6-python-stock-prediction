import dash
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
from src.components.stock.single_stock_base_layout import stock_base_layout
from linearRegression import download_stock_data, preprocess_data, split_data, train_model
import numpy as np
from sklearn.metrics import r2_score

dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    return html.Div([
        stock_base_layout(stock_id),
        html.H3("Stock Price Prediction"),
        dcc.Graph(id='prediction-graph'),
    ])

def start_predict(stock_id):
    # Main Execution - Download stock data
    ticker = stock_id  # Use the stock_id from the URL
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

    # Prepare testing data
    X_test = np.array([item[0] for item in test_data])
    y_test = np.array([item[1] for item in test_data])
    test_dates = [item[2] for item in test_data]  # Extract dates for test data

    # Train linear regression model
    model = train_model(X_train, y_train)

    # Predict values for the test set
    y_pred = model.predict(X_test)

    # Prepare data for the graph
    actual_prices = [item[1] for item in test_data]
    prediction_dates = [item[2] for item in test_data]

    # Calculate R-squared score
    r2 = r2_score(y_test, y_pred)

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prediction_dates, y=actual_prices, mode='lines', name='Actual Prices'))
    fig.add_trace(go.Scatter(x=prediction_dates, y=y_pred, mode='lines', name='Predicted Prices'))

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker}',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)

    return fig

@callback(
    Output('prediction-graph', 'figure'),
    Input('url', 'pathname')
)
def update_graph(pathname):
    stock_id = pathname.split('/')[-2]  # Extract stock_id from the URL
    return start_predict(stock_id)  # Directly return the figure
