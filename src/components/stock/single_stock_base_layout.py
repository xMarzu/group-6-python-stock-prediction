import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
import yfinance as yf
from dash import dcc
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import yfinance as yf
'''
This file contains the base layout of all single stock pages. 
'''

def stock_base_layout():
    '''
    This function will return the stock base layout used in all nested stock pages
    '''
    
    
    return (
        
        html.Div(
            [
                dcc.Location(id="url"),
                html.P("Base Layout")
            ],
            
           
        )
    )
