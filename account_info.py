import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST
import config, sqlite3
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def update_account():
    api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    acc_info = api.get_account()

    now = datetime.datetime.now().replace(second=0, microsecond=0)

    cursor.execute("INSERT INTO account_info (date, portfolio_value, cash, buying_power) VALUES (?, ?, ?, ?)",
                   (now, acc_info.portfolio_value, acc_info.cash, acc_info.buying_power))

    connection.commit()
    print('Succesfully updated account info')


def account_status():
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    # Selecting info
    account_data = cursor.execute("""
        SELECT date, portfolio_value, cash, buying_power FROM account_info ORDER BY date DESC
    """)
    account_data2 = account_data.fetchall()

    dates = [row['date'] for row in account_data2]
    portfolio_values = [row['portfolio_value'] for row in account_data2]
    dates = np.array(dates)
    portfolio_values = np.array(portfolio_values)

    # Create line graph using Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=portfolio_values))

    # Set the X and Y axis labels to an empty string
    fig.update_layout(xaxis=dict(title=''),
                      yaxis=dict(title='',
                                 autorange='reversed'))  # Set Y-axis to reversed

    # Convert the plotly figure to a JSON string
    fig_json = fig.to_json()
    return fig_json, account_data2
