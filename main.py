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

#SMA Crossover class 
class smaCrossover(Strategy):
    # Define default moving averages
    averageShort = 50
    averageLong = 200 

    def init(self):
        price = self.data.Close

        # Calculate simple moving average
        self.averageShort = self.I(SMA,price,self.averageShort)
        self.averageLong = self.I(SMA,price,self.averageLong)

    # Implement buy and sell logic based on SMA crossover
    def next(self):
        if crossover(self.averageShort,self.averageLong):
            self.buy()
        elif crossover(self.averageLong, self.averageShort):
            self.sell()


# Function to run backtest with SMA Crossover strategy based on user's input
def backtestSmaCrossover(ticker,averageShort,averageLong):
    try:
        #Download stock data from yfinance for the last 10 years
        data = yf.download(tickers=ticker,period = '10y')

        # Initialize the backtest
        bt = Backtest(data, smaCrossover, cash=10000, commission=0.002)

        # Run the backtest with user's moving average
        result = bt.run(averageShort=averageShort, averageLong=averageLong)

        print(result)
        bt.plot()

    except:
        print(f'Error downloading data for {ticker}')

backtestSmaCrossover('AAPL',50,200)

