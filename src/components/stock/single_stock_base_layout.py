import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
import yfinance as yf
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from src.components.stock.base.header_layout import header_layout
import yfinance as yf
'''
This file contains the base layout of all single stock pages. 
'''

#Whatever needs to be fetched, fetch and store in dcc store for other components to access
@callback (Output("header-store", "data"), Input("url","pathname"))
def fetch_layout_data(url : str):
        ##Fetches Name and current close pricings -> for name price layout
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
        stock_id = url.split("/")[2]
        ##Current ticker
        ticker = yf.Ticker(stock_id)
        header = fetch_header_data(ticker=ticker)
        return header
    




def stock_base_layout():
    '''
    This function will return the stock base layout used in all nested stock pages
    '''
    return (
        
        html.Div(
            [
                dcc.Location(id="url"),
                header_layout()
                
            ],
            
           
        )
    )
