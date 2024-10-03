import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
import yfinance as yf
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.components.stock.base.header_layout import header_layout
from src.components.stock.base.stock_tabs import stock_tabs
from src.components.stock.stock_layout_functions import get_stock_id_from_url
import yfinance as yf
'''
This file contains the base layout of all single stock pages. 
'''

#Whatever needs to be fetched, fetch and store in dcc store for other components to access
@callback (Output("header-store", "data"), Input("url","pathname"))
def fetch_layout_data(url : str):
        #Fetches Name and current close pricings -> for name price layout
        def fetch_header_data(ticker):
            
            #To get the percentage increase and difference, get the previous close and subtract
            def calculate_difference(close_price, prev_close):
                difference = round(close_price - prev_close,2)
                percentage_difference = round(difference/prev_close * 100,2)
                return {"difference" : difference, "percentage_difference" : percentage_difference}
            
            company_name = ticker.info['longName']
            close_price = ticker.info["currentPrice"]
            prev_close = ticker.info["previousClose"]
            difference_dic = calculate_difference(close_price, prev_close)
            header_dic = {
                "stock_name" : company_name, 
                "stock_id" : stock_id, 
                "close" : close_price
                }
            header_dic.update(difference_dic)
            print(header_dic)
        
            return header_dic
        ##Get stock ID based on the URL
        stock_id = get_stock_id_from_url(url)
        ##Current ticker
        ticker = yf.Ticker(stock_id)
        header = fetch_header_data(ticker=ticker)
        return header
    




def stock_base_layout(stock_id : str):
    """ Generates stock base layout

    Args:
        stock_id (str): id of stock

  
    """

    return (
        
        html.Div(
            [
                dcc.Location(id="url"),
                header_layout(),
                stock_tabs(stock_id=stock_id)
                
    
            ], className = "flex flex-col gap-4 mt-8"
            
           
        )
    )
