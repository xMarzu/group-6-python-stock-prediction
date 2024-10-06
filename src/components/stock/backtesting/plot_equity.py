import plotly.graph_objs as go
import plotly.express as px
from pandas import DataFrame
from datetime import timedelta

def plot_equity(equity_curve : DataFrame, main_fig):
    """Creates an equity graph based on the equity data given

    Args:
        equity_curve (df): Equity Data

    Returns:
        main_fig: Equity graph
    """
    # First graph (Equity Curve) in row 1, col 1
    equity_curve = equity_curve.reset_index()

    # Equalize the y-axis by percentages
    baseline_value = equity_curve["Equity"][0]
    equity_curve["Equity_pct"] = (equity_curve["Equity"] / baseline_value)

    # Add Equity Curve to the first subplot
    main_fig.add_trace(
        go.Scatter(
            x=equity_curve["Date"],
            y=equity_curve["Equity_pct"],
            mode='lines',
            name='Equity Percentage',
            hovertemplate="Equity: $%{customdata[0]:,.2f}<br>" +
                        "Equity Percentage: %{y}<br>" +
                        "Date: %{x}<br><extra></extra>",
            customdata=equity_curve[["Equity"]]
        ),
        row=1, col=1
    )

    # Add peak value
    peak_equity_loc = equity_curve["Equity_pct"].idxmax()
    peak_y_val = equity_curve.loc[peak_equity_loc, "Equity_pct"]
    corresponding_x_peak_value = equity_curve.loc[peak_equity_loc, "Date"]
    peak_equity_value = equity_curve.loc[peak_equity_loc, "Equity"]
    main_fig.add_trace(
        go.Scatter(
            x=[corresponding_x_peak_value],
            y=[peak_y_val],
            marker=dict(
                color="yellow",
                size=10
            ),
            name="Peak",
            hovertemplate="Equity: $%{customdata[0]:,.2f}<br>" +
                        "Equity Percentage: %{y}<br>" +
                        "Date: %{x}<br><extra></extra>",
            customdata=[[peak_equity_value]]
        ),
        row=1, col=1
    )

    # Add final value
    final_x_val = equity_curve["Date"].iloc[-1]
    final_y_val = equity_curve["Equity_pct"].iloc[-1]
    final_equity_value = equity_curve["Equity"].iloc[-1]
    main_fig.add_trace(
        go.Scatter(
            x=[final_x_val],
            y=[final_y_val],
            marker=dict(
                color="blue",
                size=10
            ),
            name="Final",
            hovertemplate="Equity: $%{customdata[0]:,.2f}<br>" +
                        "Equity Percentage: %{y}<br>" +
                        "Date: %{x}<br><extra></extra>",
            customdata=[[final_equity_value]]
        ),
        row=1, col=1
    )

    # Max drawdown
    max_drawdown_loc = equity_curve["DrawdownPct"].idxmax()
    max_drawdown_x_val = equity_curve.loc[max_drawdown_loc, "Date"]
    max_drawdown_y_val = equity_curve.loc[max_drawdown_loc, "Equity_pct"]
    max_drawdown_equity_val = equity_curve.loc[max_drawdown_loc, "Equity"]
    main_fig.add_trace(
        go.Scatter(
            x=[max_drawdown_x_val],
            y=[max_drawdown_y_val],
            marker=dict(
                color="red",
                size=10
            ),
            name="Max Drawdown",
            hovertemplate="Equity: $%{customdata[0]:,.2f}<br>" +
                        "Equity Percentage: %{y}<br>" +
                        "Date: %{x}<br><extra></extra>",
            customdata=[[max_drawdown_equity_val]]
        ),
        row=1, col=1
    )

    # Max drawdown duration
    max_drawdown_end_loc = equity_curve["DrawdownDuration"].idxmax()
    max_drawdown_end_date = equity_curve.loc[max_drawdown_end_loc, "Date"]
    max_drawdown_duration = equity_curve.loc[max_drawdown_end_loc, "DrawdownDuration"].days
    max_drawdown_start_date = max_drawdown_end_date - timedelta(days=max_drawdown_duration)
    equity_start_val = equity_curve.loc[equity_curve["Date"] == max_drawdown_start_date, "Equity_pct"].values[0]

    # Add the line to represent the max drawdown duration
    main_fig.add_trace(
        go.Scatter(
            x=[max_drawdown_start_date, max_drawdown_end_date],
            y=[equity_start_val, equity_start_val],
            mode="lines",
            line=dict(color="red", dash="dash"),
            name="Max Drawdown Duration"
        ),
        row=1, col=1
    )
    main_fig.update_yaxes(
        title_text="Equity Percentage",  # Y-axis title for the first subplot
        tickformat=".0%",  # Show y-axis as percentages without decimal
        row=1, col=1  # Specify the subplot
    )

    
    # main_fig.update_layout(
    # title="Equity Curve",
    # xaxis_title="Time",
    # yaxis_title="Equity Value",
    # legend_title="Legend",
    # legend=dict(
    # yanchor="top",
    # y=0.99,
    # xanchor="left",
    # x=0.01
    # ),
    # plot_bgcolor="#F1F1F1",
    # yaxis=dict(
    #     tickformat=".0%",  # Show y-axis as percentages without decimals
    #     )
    # )

    # return main_fig