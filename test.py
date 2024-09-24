import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import yfinance as yf
import nsepy
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import pandas as pd
import matplotlib.dates as mpl_dates
from flask import Flask, render_template
df = pd.DataFrame({
    "Stocks": ['MSFT','AAPL','KO'],
    "Value": [1,2,3]
})

# Sample data
# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    #Searchbar
    dcc.Input(
        id='search-bar',
        type='text',
        placeholder='Search for an item...'
    ),
    dcc.Graph(id='bar-chart'),
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('search-bar', 'value')
)
def update_graph(search_value):
    
    # Filter the DataFrame based on the search value
    if search_value:
        filtered_df = df[df['Stocks'].str.contains(search_value, case=False)]
    else:
        filtered_df = df
    
    # Create a bar chart
    fig = px.bar(filtered_df, x='Stocks', y='Value', title='Item Values')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)