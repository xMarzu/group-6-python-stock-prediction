import yfinance as yf
import plotly.express as px

##Get 10 years of stock data based on the stock name
def get_stock_data(stock_name, period) :
    data = yf.download(tickers=stock_name,period=period) 
    data=data.reset_index()
    return data


##Generate a simple line graph of the date and close 
def generate_line_graph(data):
    fig = px.line(data, x="Date", y="Close")
    return fig
