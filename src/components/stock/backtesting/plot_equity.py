import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta

def plot_equity(equity_curve : DataFrame):
    """Creates an equity graph based on the equity data given

    Args:
        equity_curve (df): Equity Data

    Returns:
        fig: Equity graph
    """
    equity_curve = equity_curve.reset_index()
    ##Equalize the y axis by percentages
    baseline_value = equity_curve["Equity"][0]
    equity_curve["Equity_pct"] = (equity_curve["Equity"]/ baseline_value) 

    fig = px.line(equity_curve, x="Date" , y="Equity_pct", hover_data=["Equity"])
    fig.update_traces(
    hovertemplate=
    "Equity: $%{customdata[0]:,.2f}<br>" +
                "Equity Percentage: %{y}<br>" +
                "Date: %{x}<br>" +
                "<extra></extra>",
    customdata=equity_curve[["Equity"]]
    )

   
  
  
    #Add peak value
    peak_equity_loc = equity_curve["Equity_pct"].idxmax()
    peak_y_val = equity_curve.loc[peak_equity_loc, "Equity_pct"]
    corresponding_x_peak_value = equity_curve.loc[peak_equity_loc, "Date"]
    peak_equity_value = equity_curve.loc[peak_equity_loc,"Equity"]
    fig.add_scatter(
        x= [corresponding_x_peak_value],
        y= [peak_y_val],
        marker=dict(
            color = "yellow",
            size = 10
        ),
        name= "Peak",
        hovertemplate =
                "Equity: $%{customdata[0]:,.2f}<br>" +
                "Equity Percentage: %{y}<br>" +
                "Date: %{x}<br>" +
                "<extra></extra>",
        customdata=[[peak_equity_value]]
    
    )
    
    #Add final value 
    final_x_val = equity_curve["Date"].iloc[-1]
    final_y_val = equity_curve["Equity_pct"].iloc[-1]
    final_equity_value = equity_curve["Equity"].iloc[-1]
    fig.add_scatter(
        x= [final_x_val],
        y= [final_y_val],
        marker=dict(
            color = "blue",
            size = 10
        ),
        name= "Final",
        hovertemplate =
                "Equity: $%{customdata[0]:,.2f}<br>" +
                "Equity Percentage: %{y}<br>" +
                "Date: %{x}<br>" +
                "<extra></extra>",
        customdata=[[final_equity_value]]
    
    )
    
    
    #Max Drawdown 
    max_drawdown_loc = equity_curve["DrawdownPct"].idxmax()
    max_drawdown_x_val = equity_curve.loc[max_drawdown_loc,"Date"]
    max_drawdown_y_val = equity_curve.loc[max_drawdown_loc,"Equity_pct"]
    max_drawdown_equity_val = equity_curve.loc[max_drawdown_loc,"Equity"]
    fig.add_scatter(
    x= [max_drawdown_x_val],
    y= [max_drawdown_y_val],
    marker=dict(
        color = "red",
        size = 10
    ),
    name= "Max Drawdown",
    hovertemplate =
            "Equity: $%{customdata[0]:,.2f}<br>" +
            "Equity Percentage: %{y}<br>" +
            "Date: %{x}<br>" +
            "<extra></extra>",
    customdata=[[max_drawdown_equity_val]]

    )
    
    

    # Get the end date of the max drawdown
    max_drawdown_end_loc = equity_curve["DrawdownDuration"].idxmax()
    max_drawdown_end_date = equity_curve.loc[max_drawdown_end_loc, "Date"]  
    max_drawdown_duration = equity_curve.loc[max_drawdown_end_loc, "DrawdownDuration"].days
    max_drawdown_start_date = max_drawdown_end_date - timedelta(days=max_drawdown_duration)

   
    equity_start_val = equity_curve.loc[equity_curve["Date"] == max_drawdown_start_date, "Equity_pct"].values[0]
   
    # Add the line to represent the max drawdown duration
    fig.add_scatter(
        x=[max_drawdown_start_date, max_drawdown_end_date],  # Start and end dates of the drawdown
        y=[equity_start_val, equity_start_val],  # Start and end equity values
        mode="lines",  # Line trace
        line=dict(color="red", dash="dash"),  # Same color and style as the original shape
        name="Max Drawdown Duration"  # This shows up in the legend
    )
    
    fig.update_layout(
    title="Equity Curve",
    xaxis_title="Time",
    yaxis_title="Equity Value",
    legend_title="Legend",
    legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="left",
    x=0.01
    ),
    plot_bgcolor="#F1F1F1",
    yaxis=dict(
        tickformat=".0%",  # Show y-axis as percentages without decimals
        )
    )

    return fig