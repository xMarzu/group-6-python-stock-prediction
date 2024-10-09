import os
import yfinance as yf
import nsepy
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt

from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
import os
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
from flask import Flask, render_template
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
from src.components.stock.backtesting.rsi import backtestRsi
from src.components.stock.backtesting.macd_rsi import backtestMacdRsi
from src.components.stock.backtesting.sma_crossover import backtestSmaCrossover
from src.components.navbar import navbar
import requests




external_scripts = [
    {'src': 'https://cdn.tailwindcss.com'}    
]

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], pages_folder="src/pages" , external_scripts=external_scripts, suppress_callback_exceptions=True)
app.layout = html.Div([
    navbar(),
    html.Div(
        [
            dash.page_container,
        ],className = "px-4"
    ),
], className="bg-[#F1F1F1]")
if __name__ == "__main__":
    # backtestSmaCrossover('AAPL', averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
  
    # backtestMacdRsi('AAPL', takeProfit=0.1, stopLoss=0.05, buyAmount=10)

    # backtestRsi('AAPL', takeProfit=0.1, stopLoss=0.05, buyAmount=10)
    app.run_server(debug = True)
    
# Example usage

# Number inputs for smacrossover is 6, MACDrsi has 3, RSI has 3.



