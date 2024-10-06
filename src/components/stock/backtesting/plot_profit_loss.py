import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta
import pandas as pd

def plot_profit_loss( trades):
    """Creates an profit/loss graph based on the equity data given

    Args:
        equity_curve (df): Equity Data

    Returns:
        fig: Equity graph
    """
    

 
     # Ensure the x-axis includes all dates from the dataset
    all_dates = trades["Date"]
    
    # Filter out rows where trade data (like EntryPrice, PnL, ReturnPct) is missing
    trades_with_data = trades.dropna(subset=['ReturnPct'])

    # Extract data for plotting
    entry_dates = trades_with_data["Date"]
    return_pct = trades_with_data['ReturnPct'] * 100
    
    # Determine the color for each point based on ReturnPct (green for positive, red for negative)
    entry_colors = ['green' if pct > 0 else 'red' for pct in return_pct]

    # Initialize the figure
    fig = go.Figure()

    # Set the x-axis to display all the dates, even if no trades occur on some of them
    fig.update_xaxes(type='date', range=[all_dates.min(), all_dates.max()])

    # Add scatter plot for trade entries
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


