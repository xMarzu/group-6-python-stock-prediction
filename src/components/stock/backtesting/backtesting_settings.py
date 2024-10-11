from dash import html, callback, Output,  Input, dcc,ctx, ALL, State

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



def generate_backtesting_settings():
    return (
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
                    dcc.Input(id='take-profit', type='number', step=1, placeholder='Enter Take Profit', className="p-1"),
                ],
               
                
                className="flex flex-col h-full"
              ),
               html.Div(
                  
                [
                    html.P("Stop Loss (%)", className="font-mono"),
                     dcc.Input(id='stop-loss', type='number', step=1, placeholder='Enter Stop Loss', className="p-1"),
                ],
               
                
                className="flex flex-col h-full"
              ),
                html.Div(
                  
                [
                    html.P("Buy Amount (%)", className="font-mono"),
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
      )
    )
  
    