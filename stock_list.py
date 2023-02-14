import sqlite3
import config
from datetime import date


def stock_list(stock_filter):
    connection = sqlite3.connect(config.DB_FILE)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    if stock_filter == 'new_closing_highs':
        cursor.execute("""
        SELECT * FROM (
            SELECT symbol, name, stock_id, max(close), date FROM stock_price JOIN stock 
            ON stock.id = stock_price.stock_id GROUP BY stock_id ORDER BY symbol
        ) WHERE date = ?
        """, (date.today().isoformat(),))
    elif stock_filter == 'new_closing_lows':
        cursor.execute("""
        SELECT * FROM (
            SELECT symbol, name, stock_id, min(close), date FROM stock_price JOIN stock 
            ON stock.id = stock_price.stock_id GROUP BY stock_id ORDER BY symbol
        ) WHERE date = ?
        """, (date.today().isoformat(),))
    else:
        cursor.execute("""
            SELECT id, symbol, name FROM stock ORDER BY symbol
        """)

    rows = cursor.fetchall()
    return rows
