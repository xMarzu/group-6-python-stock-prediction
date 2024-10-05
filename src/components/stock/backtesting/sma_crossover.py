from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import yfinance as yf
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

        # resultsDict = {
        #     "Trades": result['_trades'],
        #     'Total Return': result['Return [%]'],
        #     'Max Drawdow':result['Max. Drawdown [%]'],
        #     'Avg Trade Duration': result['Avg. Trade Duration'],
        #     'Win Rate': result['Win Rate [%]'],
        #     'Total Trades': result['# Trades'],
        # }
        

        # bt.plot()

        return result

    except Exception as e:
        print(f'Error downloading data for {ticker}')
        print(e)
