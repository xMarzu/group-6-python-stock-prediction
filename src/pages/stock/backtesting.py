import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.backtesting.rsi import backtestRsi
from src.components.stock.backtesting.macd_rsi import backtestMacdRsi
from src.components.stock.backtesting.plot_candlestick import plot_candlestick
from src.components.stock.backtesting.plot_volume import plot_volume
from src.components.stock.backtesting.plot_profit_loss import plot_profit_loss
from src.components.stock.stock_layout_functions import get_stock_id_from_url
from src.components.stock.backtesting.sma_crossover import backtestSmaCrossover
from src.components.stock.single_stock_base_layout import stock_base_layout
from src.components.stock.backtesting.plot_equity import plot_equity
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd


dash.register_page(__name__, path_template="/stocks/<stock_id>/backtesting")



@callback(Output("subplot-figure","figure"), [Input("run-backtest", "n_clicks"), Input("url","pathname")])
def runSMA(n_clicks, url):


   if (n_clicks == 0 ):
      
      fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            subplot_titles=("Equity Curve", "Profit/Loss", "Candlestick Chart", "Volume Chart"),
            vertical_spacing=0.03,
         )
      
      # Define layout
      layout = dict(
         title="Backtesting",
         hovermode="x unified",
         
        
      )
      

      stock_id = get_stock_id_from_url(url)
      buy_amount = 10
      # stats = backtestSmaCrossover(stock_id, averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=buy_amount)
      # stats = backtestMacdRsi(stock_id, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
      stats = backtestRsi(stock_id, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
      equity_curve = stats['Equity Curve']
      trades = stats["Trades"]
      candlestick = stats["Candlestick"]
      equity_curve = equity_curve.reset_index()
      # Merge the trades with the full dataset to expand the rows
      merged_data = pd.merge(equity_curve, trades, left_on='Date', right_on='EntryTime', how='left')
      # Keep only the relevant trade columns after merging (and the Date column)
      trade_columns = ['Date', 'EntryPrice', 'ExitPrice', 'PnL', 'ReturnPct', "ExitTime", "EntryTime"]
      filtered_trade = merged_data[trade_columns]
      
      # Plot equity curve using Plotly
      # plot_equity(equity_curve=equity_curve , main_fig=fig)
      plot_equity(equity_curve=equity_curve, main_fig= fig)
      plot_profit_loss(trades=filtered_trade,  main_fig= fig)
      plot_candlestick(candlestick, filtered_trade, fig)
      plot_volume(candlestick_data=candlestick, main_fig=fig)
      
      fig.update_layout(layout)
      return fig
   
   
   
   else:
      fig = go.Figure()
      fig.update_layout(
         title='Equity Curve',
         xaxis_title='Time',
         yaxis_title='Equity Value',
         legend=dict(x=0.02, y=0.98),
         plot_bgcolor='#F1F1F1',
         paper_bgcolor='#F1F1F1',
      )
      return fig, fig


def layout(stock_id=None, **kwargs):
    return(
      stock_base_layout(stock_id),
      html.Button("Run Backtest", id="run-backtest", n_clicks=0),
      dcc.Graph(id = "subplot-figure",  style={'height': '1500px'}),

 
      #  backtestSmaCrossover('AAPL', averageShort=7, averageLong=200, takeProfit=0.1, stopLoss=0.05, buyAmount=10)
    )