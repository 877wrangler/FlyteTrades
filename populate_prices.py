import config, sqlite3
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError
from datetime import datetime, timedelta
import pytz
import time

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()

cursor.execute("""
    SELECT id, symbol, name FROM stock 
""")

rows = cursor.fetchall()
symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']
    
api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)
timezone = pytz.timezone('America/New_York')
timeNow = datetime.now(timezone)
two_days_ago = timeNow - timedelta(days=2)

chunk_size = 100
for i in range(0, len(symbols), chunk_size):
    print(i)
    symbol_chunk = symbols[i:i+chunk_size]
    try:
        barsets = api.get_bars(symbol_chunk, timeframe="1Day",
                            start=two_days_ago.isoformat(),
                            end=None,
                            limit=200
                            )
    except APIError as e:
        invalid_symbols = e.args[0].split(': ')[1].split(',')
        for symbol in invalid_symbols:
            print(f'Invalid symbol: {symbol} {i}')
        continue
    for bar in barsets:
        print(f"procession symbol {bar.S}")

        stock_id = stock_dict[bar.S]
        cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))
    time.sleep(0.1)



connection.commit()



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

bars = get_last2Days_bars(['AAVE', 'YFI'])
for bar in bars:
    print(f'Symbol: {bar.S}')
    print(f'Timestamp: {bar.t}')
    print(f'Open: {bar.o}')
    print(f'Close: {bar.c}')
    print(f'High: {bar.h}')
    print(f'Low: {bar.l}')
    print(f'Volume: {bar.v}')
    print('---')

