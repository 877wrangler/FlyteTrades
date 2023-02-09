import sqlite3, config
import datetime as date
from datetime import date
from yfinanceapi import today_first_15min, get_daily_minbars
import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST

api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, base_url=config.API_URL)

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
# print(symbols)
current_date = date.today().isoformat()
orders = api.list_orders(status='all', after=f"{current_date}T13:30:00Z")
existing_order_symbols = [order.symbol for order in orders]


for symbol in symbols:
    opening_range_bars = today_first_15min(symbol)
    opening_range_low = opening_range_bars['Low'].min()
    opening_range_high = opening_range_bars['High'].max()
    opening_range = opening_range_high - opening_range_low

    after_opening_mins = get_daily_minbars(symbol)

    # print(opening_range_low)
    # print(opening_range_high)
    # print(opening_range)

    after_opening_range_breakout = after_opening_mins[after_opening_mins['Close'] > opening_range_high]
    # print(after_opening_range_breakout)

    if not after_opening_range_breakout.empty:
        if symbol not in existing_order_symbols:
            limit_price = round(after_opening_range_breakout.iloc[0]['Close'], 2)
            trade_time = after_opening_range_breakout.index[0].time().strftime("%H:%M:%S")
            print(f"Placing order for {symbol} at {limit_price}, closed above {opening_range_high} at {trade_time}")

            api.submit_order(
                symbol=symbol,
                side='buy',
                type='limit',
                qty=100,
                time_in_force='day',
                order_class='bracket',
                limit_price=limit_price,
                take_profit=dict(
                    limit_price=round(limit_price + opening_range, 2),
                ),
                stop_loss=dict(
                    stop_price=round(limit_price - opening_range,2),
                    limit_price=round(limit_price - opening_range, 2),
                )
            )
        else:
            print(f"Already an order for {symbol}, skipping")

