import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta
import pandas as pd

def plot_volume(candlestick_data, main_fig):
    # Determine volume colors based on close and open prices
    volume_colors = ['green' if close > open_ else 'red' for close, open_ in zip(candlestick_data['Close'], candlestick_data['Open'])]

    # Add the volume bar chart to the specific subplot (row 4, col 1)
    main_fig.add_trace(go.Bar(
        x=candlestick_data['Date'],
        y=candlestick_data['Volume'],
        marker_color=volume_colors,
        opacity=0.8,  
        showlegend=False,
        name='Volume' 
    ), row=4, col=1)

    # Update the layout for volume in the specific subplot
    main_fig.update_yaxes(title_text='Volume', row=4, col=1)  # Set the y-axis title for the volume chart
    main_fig.update_xaxes(title_text='Date', row=4, col=1)    # Set the x-axis title for the volume chart
    main_fig.update_layout(title='Volume Chart', xaxis_rangeslider_visible=False)  



