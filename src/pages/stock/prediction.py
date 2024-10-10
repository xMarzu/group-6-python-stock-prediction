import dash
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dash import html, dcc, callback, Output, Input, State
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
        dcc.Store(id='user-input-store-predict'),
        
        # Add Tabs for Linear and Prophet predictions
        dcc.Tabs(id='prediction-tabs', value='linear-tab', children=[
            dcc.Tab(label='Linear Regression', value='linear-tab', children=[
                html.H3("This prediction tool utilizes Linear Regression to forecast stock prices. To begin, please enter a start date and an end date for the model's training. Note that the model requires at least one month of data to function properly. After clicking the 'Predict Next Day' button, you will receive the predicted stock price for the following day, along with the R-squared score that indicates the model's performance."),
                dcc.Markdown(id='invalid',className="font-bold text-red-600 "),
                html.H3("Start Date:"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-start-linear',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    date=years_before),
                html.H3("End Date:"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-end-linear',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    date=formatted_date),
                html.Button('Predict Next Day', id='predict-button-linear', n_clicks=0,className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
                dcc.Markdown(id='r2_score'),
            ]),
            dcc.Tab(label='Prophet Model', value='prophet-tab', children=[
                html.H3("This prediction tool utilizes Prophet Model to forecast stock prices. To begin, please enter a start date and an end date for the model's training. Note that the model requires at least one month of data to function properly. Please also enter a date that you wish to predict. After clicking the 'Predict Day' button, you will receive the predicted stock price for the specificed day."),
                html.H3("Start Date:"),
                dcc.Markdown(id='invalid2',className="font-bold text-red-600 "),
                dcc.DatePickerSingle(
                    id='prediction-date-input-start-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    date=years_before),
                html.H3("End Date:"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-end-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    date=formatted_date),
                html.H3("Date you wish to predict:"),
                dcc.DatePickerSingle(
                    id='prediction-date-input-future-prophet',
                    placeholder='DD/MM/YYYY',
                    initial_visible_month=formatted_date,
                    date=tomorrow),
                
                html.Button('Predict Day', id='predict-button-prophet', n_clicks=0,className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
                dcc.Markdown(id='score_prophet'),
            ]),
        ]),
        
        dcc.Graph(id='prediction-graph')
    ])

@callback(
    Output('user-input-store-predict', 'data'),
    Input('prediction-date-input-start-linear', 'date'),
    Input('prediction-date-input-end-linear', 'date'),
    Input('prediction-date-input-start-prophet', 'date'),
    Input('prediction-date-input-end-prophet', 'date'),
    Input('prediction-date-input-future-prophet', 'date'),
)
def store_user_inputs_predict(prediction_date_start_linear,prediction_date_end_linear, prediction_date_start_prophet,prediction_date_end_prophet,prediction_date_future_prophet):
    return {
        'prediction_date_start_linear': prediction_date_start_linear,
        'prediction_date_end_linear': prediction_date_end_linear,
        'prediction_date_start_prophet': prediction_date_start_prophet,
        'prediction_date_end_prophet': prediction_date_end_prophet,
        'prediction_date_future_prophet': prediction_date_future_prophet,

    }


@callback(
    Output('prediction-graph', 'figure'),
    Output('r2_score','children'),
    Output('invalid','children'),
    Output('score_prophet','children'),
    Output('invalid2','children'),
    Input('url', 'pathname'),
    Input('predict-button-linear', 'n_clicks'),
    Input('predict-button-prophet', 'n_clicks'),
    Input('prediction-tabs', 'value'),
    State('user-input-store-predict', 'data')
)

def update_graph(pathname,n_clicks_linear,n_clicks_prophet,selected_tab,store_user_inputs_predict):
    # Extract stock_id from the URL
    stock_id = pathname.split('/')[-2] 
    
    r2=[]
    prophet_score=[]
    invalid=[]
    invalid2=[]
    if store_user_inputs_predict is None:
        return go.Figure(), r2,invalid,prophet_score,invalid2
    
    elif selected_tab == 'linear-tab':
        r2=[]
        prophet_score=[]
        invalid=[]
        invalid2=[]
        start_date_str = store_user_inputs_predict['prediction_date_start_linear']
        end_date_str = store_user_inputs_predict['prediction_date_end_linear']
        
        start_date = pd.to_datetime(start_date_str, errors='coerce')
        end_date = pd.to_datetime(end_date_str, errors='coerce')
        print(start_date)
        print(end_date)
        # Call the linear prediction function
        if n_clicks_linear > 0:
            if validate_dates(start_date, end_date):
                print('y')
                # If dates are valid, call the prediction function
                return start_predict_Linear(stock_id, start_date, end_date)
            else:
                # If dates are invalid, set the invalid message
                invalid = 'INVALID INPUT'
        else:
            # Handle the case when the button is not clicked
            invalid= None
    
    elif selected_tab == 'prophet-tab':
        r2=[]
        prophet_score=[]
        invalid=[]
        invalid2=[]
        # Only call the Prophet prediction function if the button has been clicked
        start_date_str = store_user_inputs_predict['prediction_date_start_prophet']
        end_date_str = store_user_inputs_predict['prediction_date_end_prophet']
        predict_date_str=store_user_inputs_predict['prediction_date_future_prophet']
        start_date = pd.to_datetime(start_date_str, errors='coerce')
        end_date = pd.to_datetime(end_date_str, errors='coerce')
        predict_date = pd.to_datetime(predict_date_str, errors='coerce')
        if n_clicks_prophet > 0:
            if validate_dates(start_date, end_date):
                # If dates are valid, call the prediction function
                return start_predict_Prophet(stock_id, start_date, end_date, predict_date)
            else:
                # If dates are invalid, set the invalid message
                invalid2 = 'INVALID INPUT'
        else:
            # Handle the case when the button is not clicked
            invalid2 = None

    # Return the figure and any other output values
    return go.Figure(), r2, invalid, prophet_score, invalid2

def start_predict_Linear(stock_id,prediction_date_start_linear,prediction_date_end_linear):
    invalid=[]
    invalid2=[]
    prophet_score=[]
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


    # Output the predicted price for the next day
    print(f"\nPredicted Stock Price for {next_day.date()}, or next possible trading day: ${predicted_price:.2f}")

    # Optionally, calculate R-squared score on the test set
    testing_x = np.array([item[0] for item in test_data])
    testing_y = np.array([item[1] for item in test_data])
    y_pred = model.predict(testing_x)
    r2 = r2_score(testing_y, y_pred)
    r2_scores = f"\n**Predicted Stock Price** for {next_day.date()}, or next possible trading day: ${predicted_price:.2f} \n\n" \
                f"**R-squared score:** {r2:.4f}  \n" \
                f"**Explanation:** The R-squared (R²) score measures how well the model predicts stock prices.  \n" \
                f"An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate."
    print("\n*** Model Performance on Test Data ***")
    print(f"R-squared score: {r2:.4f}")
    print("Explanation: The R-squared (R²) score measures how well the model predicts stock prices.")
    print("An R² score of 1.0 indicates a perfect prediction, while a score close to 0 means the model's predictions are less accurate.\n")

    # Update layout
    fig.update_layout(title=f'Actual vs Predicted Prices for {ticker} using Linear Regression',
                      xaxis_title='Date',
                      yaxis_title='Stock Price',
                      xaxis_rangeslider_visible=True)
    return fig ,r2_scores,invalid,prophet_score,invalid2

def start_predict_Prophet(stock_id, prediction_date_start_prophet,prediction_date_end_prophet,prediction_date_future_prophet):
    r2_scores=[]
    invalid2=[]
    invalid=[]
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
        prophet_score=f"\n**Predicted Stock Price** for {prediction_date_future_prophet}: ${predicted_price:.2f} \n\n"
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

    return fig,r2_scores,invalid,prophet_score,invalid2
