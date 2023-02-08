import yfinance as yf
from datetime import datetime, date
import pandas as pd
import pendulum

def today_first_15min(ticker):
    pd.options.display.max_rows=10  # To decrease printouts

    start = pendulum.parse('2023-02-08 09:30').add(hours=5)
    end = pendulum.parse('2023-02-08 09:45').add(hours=5)

    current_date = pendulum.now().date()
    start = pendulum.datetime(current_date.year, current_date.month, current_date.day, 9, 30, tz='America/New_York')
    end = pendulum.datetime(current_date.year, current_date.month, current_date.day, 9, 45, tz='America/New_York')

    data = yf.download(tickers=ticker, interval="1m", start=start, end=end)
    print(data)

