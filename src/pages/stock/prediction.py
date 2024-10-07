import dash
from datetime import date
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
from src.components.stock.single_stock_base_layout import stock_base_layout
from linearRegression import download_stock_data, preprocess_data, split_data, train_model
from prophetModel import get_stock_data,fit_prophet_model,make_prediction,evaluate_prophet_model
import numpy as np
from sklearn.metrics import r2_score

dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    # Get today's date and format into yyyy-mm-dd
    today=date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    return html.Div([
        stock_base_layout(stock_id),
        html.H3("Stock Price Prediction"),
        dcc.Graph(id='prediction-graph-linear'),
        html.H3("-"*189),
        dcc.Input(
            id='prediction-date-input',
            type='text',  # You can also use 'date' type if you want a date picker
            value=formatted_date,  # Default value
            placeholder='Enter date (YYYY-MM-DD)',
            style={'margin': '10px'}
        ),
        html.Button('Predict', id='predict-button', n_clicks=0),
        dcc.Graph(id='prediction-graph-prophet'),

    ])

@callback(
    Output('prediction-graph-linear', 'figure'),
    Output('prediction-graph-prophet', 'figure'),
    Input('url', 'pathname'),
    Input('prediction-date-input', 'value'),
    Input('predict-button', 'n_clicks')
)
def update_graph(pathname, prediction_date, n_clicks):
    stock_id = pathname.split('/')[-2]  # Extract stock_id from the URL
    linear_fig = start_predict_Linear(stock_id)
    
    # Only call the Prophet prediction function if the button has been clicked
    prophet_fig = start_predict_Prophet(stock_id, prediction_date) if n_clicks > 0 else go.Figure()
    
    return linear_fig, prophet_fig

def start_predict_Linear(stock_id):
    # Get today's date and format into yyyy-mm-dd
    today=date.today()
    formatted_date = today.strftime("%Y-%m-%d")
    # Main Execution - Download stock data
    ticker = stock_id  # Use the stock_id from the URL
    start_date = '2014-01-01'
    end_date = formatted_date
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
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Linear Regression',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)

    return fig

def start_predict_Prophet(stock_id, prediction_date):
    # Get today's date and format into yyyy-mm-dd
    today=date.today()
    formatted_date = today.strftime("%Y-%m-%d")

    ticker = stock_id
    start_date = '2014-01-01'
    end_date = formatted_date
    
    # Get stock data and fit the Prophet model
    stock_data = get_stock_data(ticker, start_date, end_date)
    model = fit_prophet_model(stock_data)
    
    # Make predictions based on the user-specified date
    predicted_price, actual_price = make_prediction(model, stock_data, end_date, prediction_date)

    # Prepare data for the bar graph
    if predicted_price is not None:
        prices = [actual_price] if actual_price is not None else [0]
        predicted_prices = [predicted_price] if predicted_price is not None else [0]

        labels = ['Actual Price', 'Predicted Price']
        fig = go.Figure()
        fig.add_trace(go.Bar(x=labels, y=[prices[0], predicted_prices[0]], name='Prices'))

        fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Prophet',
                          xaxis_title='Price Type',
                          yaxis_title='Stock Price',
                          barmode='group')

        return fig
    else:
        print("Prediction could not be made.")
        return go.Figure()  # Return an empty figure if prediction fails

