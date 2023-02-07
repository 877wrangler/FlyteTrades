import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('/home/tw/Desktop/FlyteTrades/app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("""
    SELECT symbol, company FROM stock
""")

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows]



api = tradeapi.REST('PKWAAMX739SS6VIQ4ZTB', 'H3QDKJPjvJApKsbtE5Eu7lFU7retRlV1ybMrObIV', base_url='https://paper-api.alpaca.markets')
assets = api.list_assets()

for asset in assets:
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols:
            print('Added a new stock {} {}'.format(asset.symbol, asset.name))
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()