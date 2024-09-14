import yfinance as yf
import pandas
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()

# List to store stock data
stockList = ['MSFT','AAPL','KO']
stockData = {}

# Function to get basic chart of stocks in the list
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


getChart()
getData()
