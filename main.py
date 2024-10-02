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



# List to store stock data
stockList = ['MSFT','AAPL','KO']
stockData = {}

# Math logic behind rsi indicator
def calculate_rsi(data, period=14):
    delta = data['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period, min_periods=1).mean()
    avg_loss = loss.rolling(window=period, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Get candlestick chart 
def getCandlestickChart():
    for stockSymbol in stockList:
        try:
            # Download 10 years of data for each stock
            data = yf.download(tickers=stockSymbol, period='10y')

            # Prepare the data for mplfinance candlestick chart
            data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
            data.index.name = 'Date'  # Ensure the index is named 'Date'

            # Calculate RSI 
            rsi = calculate_rsi(data)
            data['RSI'] = calculate_rsi(data)
            rsi_addplot = mpf.make_addplot(data['RSI'], panel=1, color='blue', secondary_y=True)
            
            # Plot the candlestick chart using mplfinance
            mpf.plot(data, type='candle', addplot=[rsi_addplot], mav=200, volume=True, style='charles', 
                     title=f"Candlestick Chart of {stockSymbol}", ylabel='Price', 
                     ylabel_lower='Volume', figsize=(14, 7))

        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')

# Function to get basic chart of stocks in the list
def getChart():
    for stockSymbol in stockList:
        try:
            data = yf.download(tickers=stockSymbol,period = '10y')
            ohlc = data[['Date', 'Open', 'High', 'Low', 'Close']].copy()
            fig, ax = plt.subplots()
            candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
            plt.figure(figsize=(14,5))
            plt.xlabel('Date')
            plt.ylabel('Price')
            # sns.set_style("ticks")
            # sns.lineplot(data=data,x="Date",y='Close',color='firebrick')
            # sns.despine()
            plt.title(f"The Stock Price of {stockSymbol}",size='x-large',color='blue')
            plt.show()
        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')

# Retrieve data of each stock from yfinance, append into respective lists
def getData():
    for stockSymbol in stockList:
        try:
            data = yf.download(tickers=stockSymbol,period='10y')
            # openList,closeList,volumeList = [],[],[]
            # data = yf.download(tickers=stockSymbol, period = '5d')
            # print(data['Open'])
            # for x,y,z in zip(data['Open'],data['Close'],data['Volume']):
            #     openList.append(round(x,2))
            #     closeList.append(round(y,2))
            #     volumeList.append(z)
            # print(openList,closeList,volumeList)
            # return {1: openList,2: closeList,3: volumeList}
            return data
        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')



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

