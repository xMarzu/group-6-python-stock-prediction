from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import yfinance as yf
import pandas as pd

from src.components.stock.stock_layout_functions import calculate_rsi

#MACDRSI Strategy
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
        data = data.reset_index()

        resultsDict = {
            "Trades": result['_trades'],
            'Total Return': result['Return [%]'],
            'Max Drawdow':result['Max. Drawdown [%]'],
            'Avg Trade Duration': result['Avg. Trade Duration'],
            'Win Rate': result['Win Rate [%]'],
            'Total Trades': result['# Trades'],
            "Equity Curve": result["_equity_curve"],
            "Candlestick" : data[["Date", "Open", "High", "Low", "Close", "Volume"]]
        }
        return resultsDict
    except Exception as error:
        print(f'Error fetching data for {ticker}: {error}')
