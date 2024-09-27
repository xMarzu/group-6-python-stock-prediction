import dash_bootstrap_components as dbc
##Simple navbar 
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Stocks", href="/stocks")),
        dbc.NavItem(dbc.NavLink("Prediction", href="#")),
         dbc.NavItem(dbc.NavLink("Backtesting", href="#")),
    ],
    brand="LOGO",
    brand_href="/",
    color="black",
    dark=True,
)