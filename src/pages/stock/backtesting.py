import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.single_stock_base_layout import stock_base_layout
dash.register_page(__name__, path_template="/stocks/<stock_id>/backtesting")
def layout(stock_id=None, **kwargs):
    return(
       stock_base_layout(stock_id),
       html.P("backtesting")
    )