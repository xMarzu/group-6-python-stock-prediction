import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.single_stock_base_layout import stock_base_layout


"""
This file is for generating the overview panel of each stock
It is called z_overview as we want this to be the last page rendered after all the other more specific routes
"""
dash.register_page(__name__, path_template="/stocks/<stock_id>")
def layout(stock_id=None, **kwargs):
    return(
        stock_base_layout(),
        html.P("Overview")
    )