import plotly.graph_objs as go

def plot_candlestick(candlestick_data, trades_data):
    fig = go.Figure(data=[go.Candlestick(
        x=candlestick_data['Date'],
        open=candlestick_data['Open'],
        high=candlestick_data['High'],
        low=candlestick_data['Low'],
        close=candlestick_data['Close'],
        name="Candlestick"
    )])
   # Separate trades into profits and losses
    profits = trades_data[trades_data['ReturnPct'] > 0]
    losses = trades_data[trades_data['ReturnPct'] <= 0]

    # Initialize flags for legend tracking
    profit_legend_added = False
    loss_legend_added = False

    # Create profit and loss shaded areas
    for trade in [profits, losses]:
        is_profitable = trade is profits
        color = 'rgba(0,255,0,0.3)' if is_profitable else 'rgba(255,0,0,0.3)'
        trace_name = 'Profit' if is_profitable else 'Loss'
        legend_group = 'Profit' if is_profitable else 'Loss'

        for i, single_trade in trade.iterrows():
            entry_date = single_trade['EntryTime']
            exit_date = single_trade['ExitTime']
            
            # Find the highest and lowest price during the trade period
            mask = (candlestick_data['Date'] >= entry_date) & (candlestick_data['Date'] <= exit_date)
            high_price_during_trade = candlestick_data.loc[mask, 'High'].max()
            low_price_during_trade = candlestick_data.loc[mask, 'Low'].min()

            # Add scatter plot for shaded area between entry and exit
            fig.add_trace(go.Scatter(
                x=[entry_date, exit_date, exit_date, entry_date, entry_date],
                y=[low_price_during_trade, low_price_during_trade, high_price_during_trade, high_price_during_trade, low_price_during_trade],
                fill="toself",
                fillcolor=color,
                mode="lines",
                line=dict(color=color),
                name=trace_name,
                legendgroup=legend_group,  # Group by profit or loss
                showlegend=not (profit_legend_added if is_profitable else loss_legend_added),
                hoverinfo="skip"  # This avoids displaying hover info for these shapes
            ))

            # Update the flag to indicate that the legend for this category has been added
            if is_profitable:
                profit_legend_added = True
            else:
                loss_legend_added = True

    # Customize layout
    fig.update_layout(

        xaxis_title="Date",
        yaxis_title="Price",
        xaxis_rangeslider_visible=False,
        legend_title="Trades"
    )
    return fig
