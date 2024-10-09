import dash
from dash import html, callback, Output,  Input, dcc,ctx, ALL, State
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
import dash_bootstrap_components as dbc


dash.register_page(__name__, path_template="/stocks/<stock_id>/backtesting")

@callback([Output("average-short-container", "style"), Output("average-long-container", "style")], Input("user-input-store", "data"))
def show_sma_inputs(data):
    
    if (data["strategy"] == "sma"):
       
        return {"visibility" : "visible"}, {"visibility" : "visible"}
    else:
        return {"visibility" : "hidden"}, {"visibility" : "hidden"}
    

# Callback to store user inputs
@callback(
    Output('user-input-store', 'data'),
    Input('take-profit', 'value'),
    Input('stop-loss', 'value'),
    Input('buy-amount', 'value'),
    Input('strategy-dropdown', 'value'),
    Input('average-short', 'value'),
    Input('average-long', 'value'),
)
def store_user_inputs(take_profit, stop_loss, buy_amount, strategy, average_short, average_long):
    return {
        'take_profit': take_profit,
        'stop_loss': stop_loss,
        'buy_amount': buy_amount,
        'strategy': strategy,
        'average_short': average_short,
        'average_long': average_long,
    }

@callback([Output("subplot-figure","figure") ,Output("input-invalid","style")], [Input("run-backtest", "n_clicks"), Input("url","pathname")], State('user-input-store', 'data'))
def runSMA(n_clicks, url, user_inputs):

  
 
    if (n_clicks > 0):
        strategy = user_inputs.get('strategy', 'macd')  # Default to 'macd' if strategy is None
        take_profit = user_inputs.get('take_profit')
        stop_loss = user_inputs.get('stop_loss')
        buy_amount = user_inputs.get('buy_amount')
        stock_id = get_stock_id_from_url(url)
      
        if strategy == 'sma':
            average_short = user_inputs['average_short']
            average_long = user_inputs['average_long']
            stats = backtestSmaCrossover(stock_id, averageShort=average_short, averageLong=average_long,
                                            takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
        elif strategy == 'macd':
            stats = backtestMacdRsi(stock_id, takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
        elif strategy == 'rsi':
            stats = backtestRsi(stock_id, takeProfit=take_profit, stopLoss=stop_loss, buyAmount=buy_amount)
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
        

        if (stats is None or (average_long == average_short)):
            fig = go.Figure()
            fig.update_layout(
                title='Equity Curve',
                xaxis_title='Time',
                yaxis_title='Equity Value',
                legend=dict(x=0.02, y=0.98),
                plot_bgcolor='#F1F1F1',
                paper_bgcolor='#F1F1F1',
            )
            return fig, {"visibility" : "visible"}
        
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
        return fig, {"visibility" : "hidden"}

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
        return fig, {"visibility" : "hidden"}


def layout(stock_id=None, **kwargs):
    return(
      stock_base_layout(stock_id),
      dcc.Store(id='user-input-store'),  # Store for user inputs
      html.Div(
          [
              html.Div(
                  [
                    html.P("Backtesting Strategy", className="font-mono"),
                    dcc.Dropdown(
                    id='strategy-dropdown',
                    options=[
                         {'label': 'MACD', 'value': 'macd'},
                        {'label': 'SMA', 'value': 'sma'},
                       
                        {'label': 'RSI', 'value': 'rsi'},
                    ],
                    value='macd'  # Default value
                ), 
                  ]
                 
              ),
              html.Div(
                  
                [
                    html.P("Take Profit (%)", className="font-mono"),
                    dcc.Input(id='take-profit', type='number', step=0.01, placeholder='Enter Take Profit', className="p-1"),
                ],
               
                
                className="flex flex-col h-full"
              ),
               html.Div(
                  
                [
                    html.P("Stop Loss (%)", className="font-mono"),
                     dcc.Input(id='stop-loss', type='number', step=0.01, placeholder='Enter Stop Loss', className="p-1"),
                ],
               
                
                className="flex flex-col h-full"
              ),
                html.Div(
                  
                [
                    html.P("Buy Amount", className="font-mono"),
                    dcc.Input(id='buy-amount', type='number', step=1, placeholder='Enter Buy Amount',className="p-1"),
                ],
               
                
                className="flex flex-col h-full"
              ),
                html.Div(
                  
                [
                    html.P("Average Short", className="font-mono"),
                    dcc.Input(id='average-short', type='number', step=1, placeholder='Enter Average Short', className="p-1"),
                ],
               
                
                className="flex flex-col h-full ", id="average-short-container"
              ),
                html.Div(
                  
                [
                    html.P("Average Long", className="font-mono"),
                    dcc.Input(id='average-long', type='number', step=1, placeholder='Enter Average Long', className="p-1"),
                ],
               
                
                className="flex flex-col h-full ", id="average-long-container"
              )
                
                
        
          ], className= "flex mt-4 gap-4"
      ),
    
     
    html.Button('Run Backtest', id='run-backtest', n_clicks=0, className="mt-4 bg-blue-400 rounded-lg p-2 mb-4"),
    html.P("Invalid Input!", className="font-bold text-red-600 ", id="input-invalid"),
    dcc.Graph(id = "subplot-figure",  style={'height': '1500px'}),

 
    
    )