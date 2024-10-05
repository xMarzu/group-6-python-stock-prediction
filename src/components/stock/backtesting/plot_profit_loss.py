import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta
import pandas as pd

def plot_profit_loss(equity_curve : DataFrame, trades):
    """Creates an profit/loss graph based on the equity data given

    Args:
        equity_curve (df): Equity Data

    Returns:
        fig: Equity graph
    """
    

 
    # Initialize the figure
    fig = go.Figure()
    entry_dates = trades["EntryTime"]
    exit_dates = trades["ExitTime"]
    return_pct = trades['ReturnPct'] * 100
    
    entry_colors = ['green' if pct > 0 else 'red' for pct in return_pct]

    fig.add_trace(go.Scatter(
    x=entry_dates, 
    y=return_pct,
    mode='markers',
    name='Entry Returns',
    marker=dict(color=entry_colors, size=10),
    text=return_pct,  # Display return percentage on hover
    hovertemplate='P/L: %{text:.2f}%<br>Date: %{x}<extra></extra>'
))


    return fig 


