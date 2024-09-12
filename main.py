import yfinance as yf
import pandas
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# List to store stock data
stockList = ['MSFT','AAPL','KO']
stockData = {}

def getChart():
    for stockSymbol in stockList:
        try:
            data = yf.download(tickers=stockSymbol,period = '10y')
            plt.figure(figsize=(14,5))
            sns.set_style("ticks")
            sns.lineplot(data=data,x="Date",y='Close',color='firebrick')
            sns.despine()
            plt.title(f"The Stock Price of {stockSymbol}",size='x-large',color='blue')
            plt.show()
        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')
            
def getData():
    for stockSymbol in stockList:
        try:
            data = yf.download(tickers=stockSymbol, period = '10y')
            print(data['Open'])
            print(data['Close'])
            print(data['Volume'])
        except Exception as e:
            print(f'Error fetching data for {stockSymbol}: {e}')

getData()
