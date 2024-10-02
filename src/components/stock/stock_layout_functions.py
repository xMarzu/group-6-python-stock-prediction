
import yfinance as yf

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
  