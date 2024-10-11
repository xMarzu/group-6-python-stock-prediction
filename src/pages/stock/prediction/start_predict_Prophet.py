from linearRegression import download_data, preprocess_data, split_data, train_model, predict_next_day_price, validate_dates
from prophetModel import get_stock_data, fit_prophet_model, make_prediction, evaluate_prophet_model
from sklearn.metrics import r2_score
from datetime import datetime
import numpy as np
import plotly.graph_objs as go



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
        formatted_predict_date=prediction_date_future_prophet.strftime("%Y-%m-%d")
        prophet_score=f"\n**Predicted Stock Price** for {formatted_predict_date}: ${predicted_price:.2f} \n\n"
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
