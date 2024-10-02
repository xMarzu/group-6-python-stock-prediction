import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback

##Simple navbar 
def navbar():
  
    navbar = (
    html.Div(
        children=[
            html.A(
               html.Div(
                children=[
                   
                       html.Img(
                        src='/assets/logo.png', style={'height': '50px'} 
                        ), 
                      
    
                    html.Div(
                        children = 
                        [
                            html.P("STONKS"),
                            html.P("ANALYSIS"),
                        ],
                        className="text-center"
                       
                    ),
                    
                    
                   
                ],
                className="flex items-center gap-2 text-xl font-mono" ,
            ) , href="/" 
            ),
            
         
            html.A("Stocks", className="text-center" , href="/stocks"),
            
            html.Div(
                children=[
                     html.Button(
                "Login", className="px-2 py-1"
                    ),
                    html.Button(
                        "Sign Up", className="bg-blue-300 px-2 py-1"
                    ),
                ],
                className="flex gap-4"
            ),
            
           
            
          
        ],
        className="w-full bg-white text-black flex px-4 py-2 justify-between font-mono items-center"
        
    )
)
    
    return navbar

