import dash
import pandas as pd
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from dash import html, dcc, callback, Output, Input, State
from src.components.stock.single_stock_base_layout import stock_base_layout
from src.pages.stock.prediction.prediction_switchtab import prediction_switchtab


dash.register_page(__name__, path_template="/stocks/<stock_id>/prediction")

def layout(stock_id=None, **kwargs):
    # Get today's date and format into yyyy-mm-dd
    today = date.today()
    years_before = today - relativedelta(years=10)
    tomorrow = today + timedelta(days=1)
    formatted_date = today.strftime("%Y-%m-%d")
    
    return html.Div([
        stock_base_layout(stock_id),
        prediction_switchtab(formatted_date,tomorrow,years_before)
    ])





