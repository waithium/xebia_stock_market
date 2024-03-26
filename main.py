import yfinance as yf
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

# Fetch historical stock data
ticker_symbols = ['AAPL', 'MSFT', 'GOOGL']
stock_data = yf.download(ticker_symbols, start='2023-01-01', end='2024-01-01')['Adj Close']

# Calculate daily returns
returns = stock_data.pct_change()

# Initialize Dash app
app = Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1('Stock Market Case Study Dashboard'),
    html.Div([
        dcc.Dropdown(
            id='ticker-dropdown',
            options=[{'label': symbol, 'value': symbol} for symbol in ticker_symbols],
            value=ticker_symbols[0]
        ),
        dcc.Graph(id='price-chart'),
        dcc.Graph(id='returns-chart')
    ])
])

# Define callback functions
@app.callback(
    [Output('price-chart', 'figure'), Output('returns-chart', 'figure')],
    [Input('ticker-dropdown', 'value')]
)
def update_charts(selected_ticker):
    price_fig = {
        'data': [{
            'x': stock_data.index,
            'y': stock_data[selected_ticker],
            'type': 'line',
            'name': f'{selected_ticker} Price'
        }],
        'layout': {
            'title': f'{selected_ticker} Historical Prices'
        }
    }

    returns_fig = {
        'data': [{
            'x': returns.index,
            'y': returns[selected_ticker],
            'type': 'bar',
            'name': f'{selected_ticker} Returns'
        }],
        'layout': {
            'title': f'{selected_ticker} Daily Returns'
        }
    }

    return price_fig, returns_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
