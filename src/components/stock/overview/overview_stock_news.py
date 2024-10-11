import yfinance as yf
from dash import html, callback, Output,  Input, dcc,ctx, ALL

from src.components.stock.stock_layout_functions import get_stock_id_from_url
from src.components.stock.overview.overview_stock_news_fetch import get_stock_news
import requests
from bs4 import BeautifulSoup

def get_og_image(article_url):
    """Fetch the Open Graph image from a given article URL"""
    try:
        # Fetch the HTML content of the page
        response = requests.get(article_url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find the Open Graph image tag
        og_image_tag = soup.find("meta", property="og:image")
        if og_image_tag and og_image_tag["content"]:
            return og_image_tag["content"]
    except Exception as e:
        print(f"Error fetching OG image: {e}")
    return None


##Callback for outputing the news store into the news-container
@callback(Output("news-container", "children"), Input("news-store", "data"))
def create_news(articles):
    if articles is None or len(articles) == 0:
        return html.P("No articles available.")

    # Limit to the top 5 articles
    top_articles = articles[:5]

    # Create a list of html.Div elements for the top 5 articles
    article_elements = []
    for article in top_articles:
        # Fetch the OG image from the article's URL with a timeout to avoid slow loading
        og_image_url = get_og_image(article["url"])

        article_div = html.Div(
            [
                # Display the OG image if it exists, and limit the size
                html.Img(
                    src=og_image_url, 
                    style={"width": "150px", "height": "auto", "margin-right": "15px", "border-radius": "5px", "object-fit": "cover"},
                    
                ) if  og_image_url else None,

                
                html.Div(
                    [
                        # Title with clickable link
                        html.A(
                            article["title"],
                            href=article["url"],
                            target="_blank",
                            style={"font-weight": "bold", "font-size": "18px", "margin-bottom": "10px"}
                        ),

                        # Source of the article
                        html.P(
                            f"Source: {article['source']}",
                            style={"color": "gray", "font-style": "italic", "font-size": "14px"}
                        ),

                        # Article summary
                        html.P(
                            article["summary"],
                            style={"margin-top": "10px", "font-size": "16px"}
                        ),

                        # Sentiment label and score
                        html.Div(
                            [
                                html.Span(f"Sentiment: {article['sentiment_label']}", style={"margin-right": "15px", "font-size": "14px"}),
                                html.Span(f"Score: {article['sentiment_score']:.2f}", style={"font-size": "14px"}),
                            ],
                            style={"margin-top": "5px", "color": "blue"}
                        )
                    ],
                    style={"flex": "1"}  
                )
            ],
            style={"display": "flex", "align-items": "center", "margin-bottom": "20px", "border": "1px solid #e3e3e3", "padding": "10px", "border-radius": "5px"}
        )

        article_elements.append(article_div)

    # Return the list of formatted html.Div elements
    return article_elements
   
   
    
@callback(Output("news-store", "data"), Input("url","pathname"))
def fetch_stock_news(url):
    stock_id = get_stock_id_from_url(url)
    article_list = get_stock_news(stock_id)
    return article_list




def generate_stock_news():
    """Generates a few stock news related to the current stock id based on the url
    """
    return(
        html.Div(
            [
               dcc.Store("news-store"),
               html.Div(
                   [
                       
                   ], id="news-container"
               )  
            ]
        )
       
        
    )