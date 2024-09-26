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
    close = pd.Series(data)  # Make sure we work with the correct series
    delta = close.diff()
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

    except Exception as e:
        print(f'Error downloading data for {ticker}')
        print(e)

class MacdRsiStrategy(Strategy):
    short_ema_period = 12  # Short-term EMA for MACD
    long_ema_period = 26    # Long-term EMA for MACD
    signal_line_period = 9  # EMA for the signal line in MACD
    rsi_period = 14         # Period for RSI calculation

    def init(self):
        # Convert closing prices into a Pandas Series
        closing_prices = pd.Series(self.data.Close)

        # Compute MACD values
        short_ema = closing_prices.ewm(span=self.short_ema_period, adjust=False).mean()
        long_ema = closing_prices.ewm(span=self.long_ema_period, adjust=False).mean()
        macd_value = short_ema - long_ema
        signal_value = macd_value.ewm(span=self.signal_line_period, adjust=False).mean()

        # Store the computed MACD and signal values in the strategy instance
        self.macd = self.I(lambda: macd_value)
        self.signal = self.I(lambda: signal_value)

        # Calculate RSI using the defined helper function
        self.rsi_indicator = self.I(calculate_rsi, closing_prices, self.rsi_period)

    def next(self):
        # Define trading logic based on MACD crossovers and RSI levels
        if crossover(self.macd, self.signal) and self.rsi_indicator[-1] < 70:
            self.buy()
        elif crossover(self.signal, self.macd) and self.rsi_indicator[-1] > 30:
            self.sell()

def backtest_macd_rsi(ticker_symbol):
    try:
        # Fetch historical stock data from Yahoo Finance for the past decade
        historical_data = yf.download(tickers=ticker_symbol, period='10y')

        # Create an instance of Backtest
        backtest_instance = Backtest(historical_data, MacdRsiStrategy, cash=10000, commission=0.002)

        # Execute the backtest
        backtest_results = backtest_instance.run()

        print(backtest_results)
        backtest_instance.plot()

    except Exception as error:
        print(f'Error fetching data for {ticker_symbol}: {error}')


backtestSmaCrossover('AAPL',50,200)
backtest_macd_rsi('AAPL')

