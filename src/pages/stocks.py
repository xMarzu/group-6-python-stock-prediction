import dash
from dash import html
import dash_bootstrap_components as dbc

##stocks page
dash.register_page(__name__, )

stocks=['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Define the table header
header = [html.Thead(html.Tr([html.Th("Stock Name"),html.Th("Stock Link")]))]

# Define the table body
body = html.Tbody(
    [html.Tr([html.Td(stock),html.Td(dbc.Button(f"{stock}", color="primary", class_name="mx-1",href=f"/stocks/{stock}"))]) for stock in stocks]
)

#Forming the table
table = dbc.Table(header + [body], bordered=True, striped=True, hover=True)

layout = html.Div([
    html.H1('This is our Stocks page'),
    html.Div('This is our Stocks page content.'),
    html.A(
        children=[
            html.A(
            dbc.Button(f"{stock}", color="primary", class_name="mx-1"),
            href=f"/stocks/{stock}"
            )for stock in stocks
        ],
    ),
    html.Div(
                [
                    dbc.Row([
                    dbc.Col([
                    table
                    ])
                ])
                
                ]
            ),

    

  
])