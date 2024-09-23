import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Sample data
df = pd.DataFrame({
    "Item": ["Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew"],
    "Value": [10, 15, 7, 12, 5, 20, 25, 8]
})

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    #Searchbar
    dcc.Input(
        id='search-bar',
        type='text',
        placeholder='Search for an item...'
    ),
    dcc.Graph(id='bar-chart'),
])

@app.callback(
    Output('bar-chart', 'figure'),
    Input('search-bar', 'value')
)
def update_graph(search_value):
    # Filter the DataFrame based on the search value
    if search_value:
        filtered_df = df[df['Item'].str.contains(search_value, case=False)]
    else:
        filtered_df = df
    
    # Create a bar chart
    fig = px.bar(filtered_df, x='Item', y='Value', title='Item Values')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)