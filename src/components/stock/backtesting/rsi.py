from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import yfinance as yf
from src.components.stock.stock_layout_functions import calculate_rsi

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

    except Exception as e:
        print(f'Error fetching data for {ticker}: {e}')
