import config
import alpaca_trade_api as tradeapi
from datetime import datetime, timedelta
import pytz


api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)


def get_last2Days_bars(_ticker):
    # Set the timezone you want to use
    timezone = pytz.timezone('America/New_York')

    # Get the current time in the desired timezone
    _timeNow = datetime.now(timezone)

    # Calculate the datetime 2 days ago in the desired timezone
    two_days_ago = _timeNow - timedelta(days=2)

    _bars = api.get_bars(_ticker, timeframe="1Day",
                         start=two_days_ago.isoformat(),
                         end=None,
                         limit=4
                         )
    print(_bars)
    return _bars

bars = get_last2Days_bars(['AAPL', 'MSFT'])
for bar in bars:
    print(f'Symbol: {bar.S}')
    print(f'Timestamp: {bar.t}')
    print(f'Open: {bar.o}')
    print(f'Close: {bar.c}')
    print(f'High: {bar.h}')
    print(f'Low: {bar.l}')
    print(f'Volume: {bar.v}')
    print('---')

