import pandas as pd 
import yfinance as yf
import mplfinance as mpf
import os 
def get_stock_id_from_url(url : str):
    """ Gets stock ID from a url

    Args:
        url (str): url

    Returns:
        str: stock id
    """
    ##Get stock ID based on the URL
    stock_id = url.split("/")[2]
    return stock_id


def get_stock_data(ticker: str, period : str):
    data = yf.download(tickers=ticker,period=period) 
    data= data.reset_index().to_dict('records')
    return data
  
  

# Math logic behind rsi indicator
def calculate_rsi(data, period=14):
    close = pd.Series(data)  # Make sure we work with the correct series
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

# Get candlestick chart 
def getCandlestickChart():
    stockList = ['MSFT','AAPL','KO']
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
