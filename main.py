import os
import yfinance as yf
import nsepy
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from flask import Flask, render_template
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
from src.components.navbar import navbar
import requests

external_scripts = [


    {'src': 'https://cdn.tailwindcss.com'}

]
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], pages_folder="src/pages" , external_scripts=external_scripts)



app.layout = html.Div([
    navbar(),
    html.Div(
        [
            dash.page_container,
        ],className = "px-4"
    ),
    
   
    
], className="bg-[#F1F1F1]")

if __name__ == "__main__":
    app.run_server(debug = True)

