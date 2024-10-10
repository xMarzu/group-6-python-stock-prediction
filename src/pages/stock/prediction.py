import dash
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dash import html, dcc, callback, Output, Input
import plotly.graph_objs as go
from src.components.stock.single_stock_base_layout import stock_base_layout
from linearRegression import download_data, preprocess_data, split_data, train_model, predict_next_day_price, validate_dates
from prophetModel import get_stock_data, fit_prophet_model, make_prediction, evaluate_prophet_model
from sklearn.metrics import r2_score
import numpy as np

dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    # Get today's date and format into yyyy-mm-dd
    today = date.today()
    years_before = today - relativedelta(years=10)
    tomorrow = today + timedelta(days=1)
    formatted_date = today.strftime("%Y-%m-%d")
    
    return html.Div([
        stock_base_layout(stock_id),
        html.H3("Stock Price Prediction"),
        
        # Add Tabs for Linear and Prophet predictions
        dcc.Tabs(id='prediction-tabs', value='linear-tab', children=[
            dcc.Tab(label='Linear Regression', value='linear-tab', children=[
                html.H3("Start Date:"),
                dcc.Input(
                    id='prediction-date-input-start-linear',
                    type='text', 
                    value=years_before,
                    placeholder='Enter date (YYYY-MM-DD)',
                    style={'margin': '10px'}
                ),
                html.H3("End Date:"),
                dcc.Input(
                    id='prediction-date-input-end-linear',
                    type='text', 
                    value=formatted_date,
                    placeholder='Enter date (YYYY-MM-DD)',
                    style={'margin': '10px'}
                ),
                html.Button('Predict', id='predict-button-linear', n_clicks=0),
                html.H3(id='r2_score'),
            ]),
            dcc.Tab(label='Prophet Model', value='prophet-tab', children=[
                html.H3("Start Date:"),
                dcc.Input(
                    id='prediction-date-input-start-prophet',
                    type='text', 
                    value=years_before,
                    placeholder='Enter date (YYYY-MM-DD)',
                    style={'margin': '10px'}
                ),
                html.H3("End Date:"),
                dcc.Input(
                    id='prediction-date-input-end-prophet',
                    type='text', 
                    value=formatted_date,
                    placeholder='Enter date (YYYY-MM-DD)',
                    style={'margin': '10px'}
                ),
                html.H3("Date you wish to predict:"),
                dcc.Input(
                    id='prediction-date-input-future-prophet',
                    type='text', 
                    value=tomorrow,
                    placeholder='Enter date (YYYY-MM-DD)',
                    style={'margin': '10px'}
                ),
                html.Button('Predict', id='predict-button-prophet', n_clicks=0),
            ]),
        ]),
        
        dcc.Graph(id='prediction-graph')
    ])

@callback(
    Output('prediction-graph', 'figure'),
    Output('r2_score','children'),
    Input('url', 'pathname'),
    Input('prediction-date-input-start-linear', 'value'),
    Input('prediction-date-input-end-linear', 'value'),
    Input('predict-button-linear', 'n_clicks'),
    Input('prediction-date-input-start-prophet', 'value'),
    Input('prediction-date-input-end-prophet', 'value'),
    Input('prediction-date-input-future-prophet', 'value'),
    Input('predict-button-prophet', 'n_clicks'),
    Input('prediction-tabs', 'value')
)


def update_graph(pathname,prediction_date_start_linear,prediction_date_end_linear,n_clicks_linear, prediction_date_start_prophet,prediction_date_end_prophet,prediction_date_future_prophet, n_clicks_prophet, selected_tab):
    # Extract stock_id from the URL
    stock_id = pathname.split('/')[-2] 
    r2=[]
    if selected_tab == 'linear-tab':
        start_date = pd.Timestamp(prediction_date_start_linear)
        end_date = pd.Timestamp(prediction_date_end_linear)
        # Call the linear prediction function
        if n_clicks_linear > 0 and validate_dates(start_date,end_date):
            return start_predict_Linear(stock_id,start_date,end_date)
    
    elif selected_tab == 'prophet-tab':
        # Only call the Prophet prediction function if the button has been clicked
        start_date = pd.Timestamp(prediction_date_start_prophet)
        end_date = pd.Timestamp(prediction_date_end_prophet)
        if n_clicks_prophet > 0 and validate_dates(start_date,end_date):
            return start_predict_Prophet(stock_id, start_date,end_date,prediction_date_future_prophet)
        
    # Return an empty figure if no tab is selected
    return go.Figure(),r2

def start_predict_Linear(stock_id,prediction_date_start_linear,prediction_date_end_linear):
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

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Linear Regression',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)
    
    # Predict the next day's stock price using the last available sequence
    last_sequence = stock_data.iloc[-sequence_length:].values  # Last 10 days before the last available date
    last_date = dates[-1]  # The last date in the dataset

    # Debug prints
    print(f"\nData Sequence used for prediction: {last_sequence}")
    print(f"Last date in the dataset: {last_date}")

    # Predict stock price for the next day
    predicted_price, next_day = predict_next_day_price(model, last_sequence, last_date)

    # Output the predicted price for the next day
    print(f"\nPredicted Stock Price for {next_day.date()}, or next possible trading day: ${predicted_price:.2f}")

    # Optionally, calculate R-squared score on the test set
    testing_x = np.array([item[0] for item in test_data])
    testing_y = np.array([item[1] for item in test_data])
    y_pred = model.predict(testing_x)
    r2 = r2_score(testing_y, y_pred)
    r2_scores = f'R-squared score: {r2:.4f}'
    print("\n*** Model Performance on Test Data ***")
    print(f"R-squared score: {r2:.4f}")
    print("Explanation: The R-squared (R²) score measures how well the model predicts stock prices.")
    print("An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate.\n")

    return fig ,r2_scores

def start_predict_Prophet(stock_id, prediction_date_start_prophet,prediction_date_end_prophet,prediction_date_future_prophet):
    # Main Execution
    ticker = stock_id
    start_date = prediction_date_start_prophet
    end_date = prediction_date_end_prophet

    # Get stock data and fit the Prophet model
    stock_data = get_stock_data(ticker, start_date, end_date)
    model = fit_prophet_model(stock_data)

    # Make predictions based on the user-specified date
    predicted_price, actual_price = make_prediction(model, stock_data, str(end_date), str(prediction_date_future_prophet))

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
            x=[prediction_date_future_prophet],
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
