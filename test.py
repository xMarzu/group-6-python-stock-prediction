import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import yfinance as yf
import nsepy
from nsepy import get_history
from datetime import date
import matplotlib.pyplot as plt
import mplfinance as mpf
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mpl_dates
from flask import Flask, render_template
import plotly.graph_objs as go

# Sample data
data = {
    'x': [1, 2, 3, 4, 5],
    'y1': [2, 3, 5, 7, 11],
    'y2': [1, 2, 4, 8, 16],
    'y3': [5, 3, 4, 2, 1],
}

# Create a DataFrame
df = pd.DataFrame(data)

# Define line labels
line_labels = ['Line 1', 'Line 2', 'Line 3']
y_columns = ['y1', 'y2', 'y3']

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div(children=[
    html.H1(children='Interactive Line Graph with Search'),

    dcc.Input(
        id='search-bar',
        type='text',
        placeholder='Search for line (Line 1, Line 2, Line 3)...',
        style={'margin-bottom': '20px'}
    ),

    dcc.Graph(id='line-graph'),

    html.Div(id='output-message')
])

# Callback to update the graph based on the search input
@app.callback(
    Output('line-graph', 'figure'),
    Output('output-message', 'children'),
    Input('search-bar', 'value')
)
def update_graph(search_value):
    # Create a figure object
    figure = go.Figure()

    # Determine which lines to include based on the search input
    if search_value:
        filtered_labels = [label for label in line_labels if search_value.lower() in label.lower()]
    else:
        filtered_labels = line_labels

    # Add traces for the selected lines
    for i, label in enumerate(filtered_labels):
        figure.add_trace(go.Scatter(
            x=df['x'],
            y=df[y_columns[i]],
            mode='lines+markers',
            name=label
        ))

    # Update layout
    figure.update_layout(
        title='Line Graph Example',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price'},
    )

    # Output message if no lines are found
    if not filtered_labels:
        return figure, "No lines found matching the search."

    return figure, ""

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
