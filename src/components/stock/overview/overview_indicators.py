import yfinance as yf
from dash import html, callback, Output,  Input, dcc,ctx, ALL
from src.components.stock.stock_layout_functions import format_large_number, get_stock_id_from_url
from datetime import datetime
import math




##Callback for updating each of the overview indicators when the overview storeis updated at first load of webpage 
@callback([Output("overview-market-cap", "children"), Output("overview-revenue", "children"),
           Output("overview-net-income", "children"), Output("overview-shares-out", "children"),
           Output("overview-eps", "children"),Output("overview-pe-ratio", "children"),
           Output("overview-forward-pe", "children"),Output("overview-dividend", "children"),
           Output("overview-dividend-date", "children"),Output("overview-volume", "children"),
           Output("overview-open", "children"),Output("overview-previous-close", "children"),
           Output("overview-days-range", "children"),Output("overview-52-range", "children"),
           Output("overview-beta", "children"),Output("overview-analysts", "children"),
           Output("overview-price-target", "children"),Output("overview-payout-ratio", "children"),       
           ], Input("overview-store", "data"))
def fetch_overview_indicators(data):
    
    return (data["market_cap"], data["revenue"], data["net_income"],data["shares_out"], data["eps"], data["pe_ratio"],
            data["forward_pe"], data["dividend_rate"], data["dividend_date"], data["volume"], data["stock_open"], 
            data["stock_prev_close"], data["day_range"], data["_52_week_range"], data["beta"], data["analysts"], data["price_target"], data["payout_ratio"])


#Fetch and store the data that is needed in the inidcators into the overview store
@callback(Output("overview-store", "data"), Input("url","pathname"))
def allocate_overview_indicators(url):
    
    
 
    stock_id = get_stock_id_from_url(url)
    ticker = yf.Ticker(stock_id)
   
    info = ticker.info

    
    # Safely extract data with default "NA" if key does not exist
    market_cap = format_large_number( info.get("marketCap", "NA"))
    revenue = format_large_number(info.get("totalRevenue", "NA"))
    net_income = format_large_number(info.get("netIncomeToCommon", "NA"))
    shares_out = format_large_number(info.get("sharesOutstanding", "NA"))
    eps = info.get("trailingEps", "NA")
    pe_ratio = info.get("pegRatio", "NA")
    forward_pe = info.get("forwardPE", "NA")
    
    # Handle dividend and yield calculation safely
    dividend_rate = info.get("dividendRate", "NA")
    dividend_yield = info.get("dividendYield", "NA")
    if dividend_rate != "NA" and dividend_yield != "NA":
        dividend_rate = f"${dividend_rate:.2f} ({dividend_yield*100:.2f}%)"
    else:
        dividend_rate = "NA"

    # Handle dividend date safely if it's in Unix format
    dividend_date = info.get("exDividendDate", "NA")
    if dividend_date != "NA":
        dividend_date = datetime.fromtimestamp(dividend_date)
        # dividend_date = datetime.fromisoformat(dividend_date)
        dividend_date = dividend_date.date()
        dividend_date = dividend_date.strftime('%Y-%m-%d')
        
    else:
        dividend_date = "NA"

    volume = format_large_number( info.get("averageVolume", "NA"))
    stock_open = f'{info["open"]:.3f}' if isinstance(info.get("open"), (int, float)) else 'NA'
    stock_prev_close = f'{info["previousClose"]:.3f}' if isinstance(info.get("previousClose"), (int, float)) else 'NA'
    
    # Handle day range safely
    day_low = f'{info["dayLow"]:.3f}' if isinstance(info.get("dayLow"), (int, float)) else 'NA'
    day_high = f'{info["dayHigh"]:.3f}' if isinstance(info.get("dayHigh"), (int, float)) else 'NA'
    day_range = f"{day_low} - {day_high}" if day_low != "NA" and day_high != "NA" else "NA"
    
    # Handle 52-week range safely
    _52_week_low = f'{info["fiftyTwoWeekLow"]:.3f}' if isinstance(info.get("fiftyTwoWeekLow"), (int, float)) else 'NA'
    _52_week_high = f'{info["fiftyTwoWeekHigh"]:.3f}' if isinstance(info.get("fiftyTwoWeekHigh"), (int, float)) else 'NA'
    _52_week_range = f"{_52_week_low} - {_52_week_high}" if _52_week_low != "NA" and _52_week_high != "NA" else "NA"
    
    beta = f'{info["beta"]:.2f}' if isinstance(info.get("beta"), (int, float)) else 'NA'
    
    analysts = (info.get("recommendationKey", "NA")).upper()
    price_target = info.get("targetMeanPrice", "NA")
    payout_ratio = f'{info["payoutRatio"]:.3f}' if isinstance(info.get("payoutRatio"), (int, float)) else 'NA'
    return {"market_cap" : market_cap, "revenue" : revenue, "net_income" : net_income, "shares_out" : shares_out, "eps" : eps, "pe_ratio" : pe_ratio, 
        "forward_pe" : forward_pe, "dividend_rate" : dividend_rate, "dividend_date" : dividend_date, "volume" : volume, "stock_open" : stock_open,
        "stock_prev_close" : stock_prev_close, "day_range" : day_range, "_52_week_range" : _52_week_range, "beta" : beta, "analysts" : analysts, 
        "price_target" : price_target, "payout_ratio" : payout_ratio}


def generate_overview_indicators(stock_id : str):
    """ Generates the overview indicators
    """
    return (
        html.Div(
            [
                html.Div(
                [
                    html.P("Market Cap", className="text-left"),
                    html.P("" ,className="font-bold" ,id="overview-market-cap"),
                    html.P("Revenue (ttm)",className="text-left"),
                    html.P("" ,className="font-bold" ,id="overview-revenue"),
                    html.P("Net Income (ttm)", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-net-income"),
                    html.P("Shares Out",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-shares-out"),
                    html.P("EPS (ttm)", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-eps"),
                    html.P("PE Ratio",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-pe-ratio"),
                    html.P("Forward PE", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-forward-pe"),
                    html.P("Dividend",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-dividend"),
                    html.P("Ex-Dividend Date",className="text-left"),
                    html.P("" ,className="font-bold", id= "overview-dividend-date"),
                    
                    
                ],className="grid grid-cols-2 gap-3 text-right"
            ),  
            html.Div(
                [
                    html.P("Volume", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-volume"),
                    html.P("Open",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-open"),
                    html.P("Previous Close", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-previous-close"),
                    html.P("Day's Range",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-days-range"),
                    html.P("52-Week Range", className="text-left"),
                    html.P("" ,className="font-bold", id="overview-52-range"),
                    html.P("Beta",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-beta"),
                    html.P("Analysts", className="text-left"),
                    html.P("" ,className="font-bold",  id="overview-analysts"),
                    html.P("Price Target",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-price-target"),
                    html.P("Payout Ratio",className="text-left"),
                    html.P("" ,className="font-bold", id="overview-payout-ratio"),
                ],className="grid grid-cols-2 gap-3 text-right"
                
            )
            ], className="flex gap-4 min-w-[35%]"
           
        )
        
       
        
        
        

    )