import yfinance as yf
import pendulum

def today_first_15min(ticker):
    # pd.options.display.max_rows=10  # To decrease printouts

    current_date = pendulum.now().date()
    start = pendulum.datetime(current_date.year, current_date.month, current_date.day, 9, 30, tz='America/New_York')
    end = pendulum.datetime(current_date.year, current_date.month, current_date.day, 9, 45, tz='America/New_York')

    data = yf.download(tickers=ticker, interval="1m", start=start, end=end)
    return data

