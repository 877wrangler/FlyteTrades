import polygon
from polygon import RESTClient


from datetime import date

KEY = '2w4sI8BiTXK6sKcw9rp6Q5P_qeLVNQGp'

client = polygon.StocksClient(KEY)

# current price for a stock
current_price = client.get_current_price('AMD')

# LAST QUOTE for a stock
last_quote = client.get_last_quote('AMD')

print(last_quote)