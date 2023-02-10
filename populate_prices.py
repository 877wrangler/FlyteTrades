import config, sqlite3, time, pytz, talib
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import APIError
from datetime import datetime, timedelta, date
import numpy as np

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
current_date = date.today()
two_days_ago = timeNow - timedelta(days=1)

# symbols = ['MSFT'] # Temp override to test TA
chunk_size = 190
for i in range(0, len(symbols), chunk_size):
    print(i)
    symbol_chunk = symbols[i:i + chunk_size]
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

    # Testing SMA
    recent_closes = [bar.c for bar in barsets] # Store recent closes
    recent_closes = np.array(recent_closes)
    print(len(recent_closes))

    for bar in barsets:
        print(f"processing symbol {bar.S}")
        # print(barsets[0]) # For testing TA

        if len(recent_closes) >= 50 and current_date == bar.t.date():
            sma_20 = talib.SMA(recent_closes, timeperiod=20)[-1]
            sma_50 = talib.SMA(recent_closes, timeperiod=50)[-1]
            rsi_14 = talib.RSI(recent_closes, timeperiod=14)[-1]
        else:
            sma_20, sma_50, rsi_14 = None, None, None
        print(rsi_14)

        stock_id = stock_dict[bar.S]
        print(bar)
        cursor.execute("""
            INSERT INTO stock_price (stock_id, date, open, high, low, close, volume, sma_20, sma_50, rsi_14)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v, sma_20, sma_50, rsi_14))
    time.sleep(0.1)

connection.commit()
