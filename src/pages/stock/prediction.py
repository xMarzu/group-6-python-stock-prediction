import dash
import pandas as pd
from datetime import date, timedelta
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
from src.components.stock.single_stock_base_layout import stock_base_layout
from linearRegression import download_data, preprocess_data, split_data, train_model, predict_next_day_price
from prophetModel import get_stock_data, fit_prophet_model, make_prediction, evaluate_prophet_model
import numpy as np

dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    # Get today's date and format into yyyy-mm-dd
    today = date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    
    return html.Div([
        stock_base_layout(stock_id),
        html.H3("Stock Price Prediction"),
        dcc.Input(
            id='prediction-date-input',
            type='text', 
            value=formatted_date,
            placeholder='Enter date (YYYY-MM-DD)',
            style={'margin': '10px'}
        ),
        html.Button('Predict', id='predict-button', n_clicks=0),
        
        # Add Tabs for Linear and Prophet predictions
        dcc.Tabs(id='prediction-tabs', value='linear-tab', children=[
            dcc.Tab(label='Linear Regression', value='linear-tab'),
            dcc.Tab(label='Prophet Model', value='prophet-tab'),
        ]),
        
        dcc.Graph(id='prediction-graph')
    ])

@callback(
    Output('prediction-graph', 'figure'),
    Input('url', 'pathname'),
    Input('prediction-date-input', 'value'),
    Input('predict-button', 'n_clicks'),
    Input('prediction-tabs', 'value')
)
def update_graph(pathname, prediction_date, n_clicks, selected_tab):
    # Extract stock_id from the URL
    stock_id = pathname.split('/')[-2] 

    if selected_tab == 'linear-tab':
        # Call the linear prediction function
        return start_predict_Linear(stock_id)
    
    elif selected_tab == 'prophet-tab':
        # Only call the Prophet prediction function if the button has been clicked
        if n_clicks > 0:
            return start_predict_Prophet(stock_id, prediction_date)
        
    # Return an empty figure if no tab is selected
    return go.Figure()  

def start_predict_Linear(stock_id):
    date_list = pd.date_range(start='2014-01-01', end=pd.Timestamp.today()).date
    date_list = list(date_list)
    print(date_list)
    # Calculate yesterday's date
    today = date.today()
    yesterday = today - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")
    # Main Execution - Download stock data
    ticker = stock_id 
    start_date = '2014-01-01'
    end_date = formatted_date
    stock_data, dates = download_data(ticker, start_date, end_date)

    # Preprocess data - Creates sequences of 10 days of stock prices, target on the 11th day
    sequence_length = 10
    data_sequences = preprocess_data(stock_data, sequence_length)

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

    # Create a date range for the test data
    test_start_date = pd.to_datetime(stock_data.index[-len(test_data):]).date
    prediction_dates = pd.date_range(start=test_start_date[0], periods=len(test_data)).date

    # Plotting
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=prediction_dates, y=actual_prices, mode='lines', name='Actual Prices'))
    fig.add_trace(go.Scatter(x=prediction_dates, y=y_pred, mode='lines', name='Predicted Prices'))

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Linear Regression',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)

    return fig

def start_predict_Prophet(stock_id, prediction_date):
    # Calculate yesterday's date
    today = date.today()
    yesterday = today - timedelta(days=1)
    formatted_date = yesterday.strftime("%Y-%m-%d")

    ticker = stock_id
    start_date = '2020-01-01'
    end_date = formatted_date

    # Get stock data and fit the Prophet model
    stock_data = get_stock_data(ticker, start_date, end_date)
    model = fit_prophet_model(stock_data)

    # Make predictions based on the user-specified date
    predicted_price, actual_price = make_prediction(model, stock_data, end_date, prediction_date)

    # Prepare data for the line graph
    actual_prices = stock_data['y'].values[-len(stock_data):]  # Assuming 'y' contains actual prices
    prediction_dates = stock_data['ds'].values[-len(stock_data):]  # Assuming 'ds' contains dates

    # Create a new figure
    fig = go.Figure()

    # Plot actual prices
    fig.add_trace(go.Scatter(
        x=prediction_dates,
        y=actual_prices,
        mode='lines',
        name='Actual Prices'
    ))

    # Plot predicted price
    if predicted_price is not None:
        # Append the predicted price to the end date
        fig.add_trace(go.Scatter(
            x=[prediction_date],
            y=[predicted_price],
            mode='markers+lines',
            name='Predicted Price',
            marker=dict(size=10)
        ))

    # Update layout
    fig.update_layout(
        title=f'Actual vs Predicted Prices for {ticker} using Prophet',
        xaxis_title='Date',
        yaxis_title='Stock Price',
        xaxis_rangeslider_visible=True
    )

    return fig
