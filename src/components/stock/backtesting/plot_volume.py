import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta
import pandas as pd

def plot_volume(candlestick_data):
 
   
    volume_colors = ['green' if close > open_ else 'red' for close, open_ in zip(candlestick_data['Close'], candlestick_data['Open'])]

    volume_fig = go.Figure(data=go.Bar(
        x=candlestick_data['Date'],
        y=candlestick_data['Volume'],
        marker_color=volume_colors,
        opacity=0.8,  
        showlegend=False  # Disable legend
    ))

    # Update the layout for volume
    volume_fig.update_layout(
        title='Volume Chart',
        xaxis_title='Date',
        yaxis_title='Volume',
        xaxis_rangeslider_visible=False
    )

    return volume_fig

