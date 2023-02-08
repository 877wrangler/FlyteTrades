import sqlite3
import config
import datetime as date
from yfinanceapi import today_first_15min

connection = sqlite3.connect(config.DB_FILE)
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
# Get strategy record
cursor.execute("""
    SELECT id FROM strategy WHERE name = 'opening_range_breakout'
""")
strategy_id = cursor.fetchone()['id']
# Get stock list for this strategy
cursor.execute("""
    SELECT symbol, name FROM stock JOIN stock_strategy ON stock_strategy.stock_id = stock.id
    WHERE stock_strategy.strategy_id = ?
""", (strategy_id,))

stocks = cursor.fetchall()
symbols = [stock['symbol'] for stock in stocks]
print(symbols)

for symbol in symbols:
    opening_range_bars = today_first_15min(symbol)
    opening_range_low = opening_range_bars['Low'].min()
    opening_range_high = opening_range_bars['High'].max()
    opening_range = opening_range_high - opening_range_low
    print(opening_range_low)
    print(opening_range_high)
    print(opening_range)

