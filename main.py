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
import os
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
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

# Math logic behind rsi indicator
def calculate_rsi(data, period=14):
    close = pd.Series(data)  # Make sure we work with the correct series
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

stockList = ['MSFT','AAPL','KO']
stockData = {}
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
            openList,closeList,volumeList = [],[],[]
            data = yf.download(tickers=stockSymbol, period = '5d')
            print(data['Open'])
            for x,y,z in zip(data['Open'],data['Close'],data['Volume']):
                openList.append(round(x,2))
                closeList.append(round(y,2))
                volumeList.append(z)
            print(openList,closeList,volumeList)

        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')

# Download CSV file containing stock data into users download folder
def downloadCSV(ticker):
    try:
        #Download stock data from yfinance for the last 10 years
        data = yf.download(tickers=ticker,period = '10y')

        #Set download path for user's download folder
        download_folder = os.path.expanduser('~/Downloads')
        csv_file_path = os.path.join(download_folder, f'{ticker}_data.csv')

        #Save the downloaded data into a CSV file
        data.to_csv(csv_file_path)

        print(f"Data for {ticker} saved to {csv_file_path}")

    except:
        print(f'Error downloading data for {ticker}')

# Update the SMA Crossover class to check for stop loss and take profit before selling
class smaCrossover(Strategy): 
    averageShort = 50 
    averageLong = 200 

    # Initialize fields for useers inputs
    takeProfit = None 
    stopLoss = None 
    buyAmount = None 
    entryPrice = None  

    def init(self): 
        price = self.data.Close 
        # Calculate moving averages 
        self.averageShort = self.I(SMA, price, self.averageShort) 
        self.averageLong = self.I(SMA, price, self.averageLong) 
 
    def next(self):
        price = self.data.Close[-1]  # Current price 
         
        # If there's no position, check for a crossover to buy 
        if not self.position: 
            if crossover(self.averageShort, self.averageLong): 
                if self.buyAmount is not None: 
                    # Determine size based on cash or fixed amount 
                    if self.buyAmount <= 1: 
                        cash = self.broker.cash 
                        size = (cash * self.buyAmount) / price
                    else: 
                        size = self.buyAmount 
                     
                    self.buy(size=size)  # Place buy order 
                    self.entryPrice = price  # Set entry price after buying 
 
        # If there's a position, check stop loss and take profit 
        elif self.position: 
            if self.entryPrice is not None and self.takeProfit is not None and self.stopLoss is not None: 
                # Calculate take profit and stop loss price levels 
                takeProfitPrice = self.entryPrice * (1 + self.takeProfit) 
                stopLossPrice = self.entryPrice * (1 - self.stopLoss)
                
                # Check if current price hits take profit or stop loss levels
                if price >= takeProfitPrice:
                    self.sell(size=self.position.size)  # Sell all
                    
                elif price <= stopLossPrice:
                    self.sell(size=self.position.size)  # Sell all
                    
# Function to run backtest with SMA Crossover strategy based on user's input
def backtestSmaCrossover(ticker,averageShort,averageLong,takeProfit,stopLoss,buyAmount):
    try:
        #Download stock data from yfinance for the last 10 years
        data = yf.download(tickers=ticker,period = '10y')

        # Update SMA Strategy class with user-defined buy size,take profit and stoploss
        smaCrossover.takeProfit = takeProfit
        smaCrossover.stopLoss = stopLoss
        smaCrossover.buyAmount = buyAmount

        # Initialize the backtest
        bt = Backtest(data, smaCrossover, cash=10000, commission=0.002)

        # Run the backtest with user's moving average
        result = bt.run(averageShort=averageShort, averageLong=averageLong)

        resultsDict = {
            "Trades": result['_trades'],
            'Total Return': result['Return [%]'],
            'Max Drawdow':result['Max. Drawdown [%]'],
            'Avg Trade Duration': result['Avg. Trade Duration'],
            'Win Rate': result['Win Rate [%]'],
            'Total Trades': result['# Trades'],
        }

        bt.plot()

        return resultsDict

    except Exception as e:
        print(f'Error downloading data for {ticker}')
        print(e)

#MACDRSI Strategy
class MACDRsi(Strategy):
    ema_short_period = 12
    ema_long_period = 26
    signal_line_period = 9
    rsi_period = 14

    # Initialize fields for useers inputs
    takeProfit = None 
    stopLoss = None 
    buyAmount = None 
    entryPrice = None  

    def init(self):
        price = self.data.Close
        closing_prices = pd.Series(self.data.Close)
        ema_short = closing_prices.ewm(span=self.ema_short_period, adjust=False).mean()
        ema_long = closing_prices.ewm(span=self.ema_long_period, adjust=False).mean()
        macd = ema_short - ema_long
        signal_value = macd.ewm(span=self.signal_line_period, adjust=False).mean()
        self.macd = self.I(lambda: macd)
        self.signal = self.I(lambda: signal_value)
        self.rsi_indicator = self.I(calculate_rsi, closing_prices, self.rsi_period)

    def next(self):
        price = self.data.Close[-1] # Current price

        # If there's no position, check for a macd signal and rsi indicattor to be under 70
        if not self.position:
            if crossover(self.macd, self.signal) and self.rsi_indicator[-1] < 70:
                if self.buyAmount <= 1:
                    cash = self.broker.cash
                    size = (cash * self.buyAmount) / price
                else:
                    size = self.buyAmount

                self.buy(size=size) # Place buy order 
                self.entryPrice = price # Set entry price after buying 
                self.buy()

        elif self.position:
            if self.entryPrice is not None and self.takeProfit is not None and self.stopLoss is not None: 
                # Calculate take profit and stop loss price levels
                takeProfitPrice = self.entryPrice * (1 + self.takeProfit) 
                stopLossPrice = self.entryPrice * (1 - self.stopLoss)
                # Check if current price hits take profit or stop loss levels
                if price >= takeProfitPrice:
                    self.sell(size=self.position.size) #Sell all
                elif price <= stopLossPrice:
                    self.sell(size=self.position.size)


#Backtesting MACDRSI strategy
def backtestMacdRsi(ticker,takeProfit,stopLoss,buyAmount):
    try:
        #Download stock data from yfinance for the last 10 years
        data = yf.download(tickers=ticker, period='10y')

        # Update SMA Strategy class with user-defined buy size,take profit and stoploss
        MACDRsi.takeProfit = takeProfit
        MACDRsi.stopLoss = stopLoss
        MACDRsi.buyAmount = buyAmount

        # Initialize the backtest
        bt = Backtest(data, MACDRsi, cash=10000, commission=0.002)

        result = bt.run()

        resultsDict = {
            "Trades": result['_trades'],
            'Total Return': result['Return [%]'],
            'Max Drawdow':result['Max. Drawdown [%]'],
            'Avg Trade Duration': result['Avg. Trade Duration'],
            'Win Rate': result['Win Rate [%]'],
            'Total Trades': result['# Trades'],
        }

        bt.plot()
        
        return resultsDict
    except Exception as error:
        print(f'Error fetching data for {ticker}: {error}')

class RSI(Strategy):
    period_rsi = 14
    overbought_rsi = 70
    oversold_rsi = 30

    # Initialize fields for useers inputs
    takeProfit = None 
    stopLoss = None 
    buyAmount = None 
    entryPrice = None

    def init(self):

        price = self.data.Close
        self.rsi = self.I(calculate_rsi, price, self.period_rsi)

    def next(self):
        price = self.data.Close[-1] # Current price
        # If there's no position, check for an oversold or overbought situation
        if not self.position:
            if self.rsi[-1] < self.oversold_rsi: #Purchase when the RSI is below 30, meaning it is oversold
                if self.buyAmount is not None: 
                    # Determine size based on cash or fixed amount 
                    if self.buyAmount <= 1: 
                        cash = self.broker.cash 
                        size = (cash * self.buyAmount) / price 
                    else: 
                        size = self.buyAmount 
                     
                    self.buy(size=size)  # Place buy order 
                    self.entryPrice = price  # Set entry price after buying 

        elif self.position:
            if self.entryPrice is not None and self.takeProfit is not None and self.stopLoss is not None: 
                # Calculate take profit and stop loss price levels
                takeProfitPrice = self.entryPrice * (1 + self.takeProfit) 
                stopLossPrice = self.entryPrice * (1 - self.stopLoss)
                # Check if current price hits take profit or stop loss levels
                if price >= takeProfitPrice:
                    self.sell(size=self.position.size) #Sell all
                elif price <= stopLossPrice:
                    self.sell(size=self.position.size)

#Backtesting using RSI Strategy
def backtestRsi(ticker,takeProfit,stopLoss,buyAmount):
    try:
        # Download stock data from yfinance for the last 10 years
        data = yf.download(tickers=ticker, period='10y')

        # update RSI Strategy class with user-defined buy sie,takeProfit and stoploss
        RSI.takeProfit = takeProfit
        RSI.stopLoss = stopLoss
        RSI.buyAmount = buyAmount
        
        bt = Backtest(data, RSI, cash=10000, commission=0.002)

        result = bt.run()

        resultsDict = {
            "Trades": result['_trades'],
            'Total Return': result['Return [%]'],
            'Max Drawdow':result['Max. Drawdown [%]'],
            'Avg Trade Duration': result['Avg. Trade Duration'],
            'Win Rate': result['Win Rate [%]'],
            'Total Trades': result['# Trades'],
        }

        bt.plot()
        
        return resultsDict

    except Exception as e:
        print(f'Error fetching data for {ticker}: {e}')

# Example usage

# Number inputs for smacrossover is 6, MACDrsi has 3, RSI has 3.

backtestSmaCrossover('AAPL', averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
# backtestMacdRsi('AAPL', takeProfit=0.1, stopLoss=0.05, buyAmount=10)
# backtestRsi('AAPL', takeProfit=0.1, stopLoss=0.05, buyAmount=10)
