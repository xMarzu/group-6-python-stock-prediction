import math
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
  
  

def calculate_rsi(data, period=14):
    # Ensure data is a pandas Series
    close = pd.Series(data)
    
    # Calculate price differences
    delta = close.diff()
    
    # Separate gains and losses
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    # Calculate the average gain and average loss
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    # Calculate the relative strength (RS)
    rs = avg_gain / avg_loss

    # Calculate the RSI
    rsi = 100 - (100 / (1 + rs))

    # Return the RSI, ensuring the output has the same length as the input
    return rsi.fillna(0)  # Fill NaN values with 0 for better compatibility
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




def format_large_number(number):
    """Formats a large number into K, M, B , T, etc.

    Args:
        number (float): Number you want to reformat 

    Returns:
        number (float): Reformatted Number
    """
    suffixes = ['', 'K', 'M', 'B', 'T']
    if number == 0:
        return "0"
    
    # Calculate the log base 1000 to determine the index for the suffix
    magnitude = int(math.floor(math.log10(abs(number)) / 3))
    
    # Limit the index to the available suffixes
    magnitude = min(magnitude, len(suffixes) - 1)
    
    # Scale the number down and format with the correct suffix
    scaled_number = number / (10 ** (3 * magnitude))
    return f"{scaled_number:.2f}{suffixes[magnitude]}"