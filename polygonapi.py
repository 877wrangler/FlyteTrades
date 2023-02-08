from polygon import RESTClient
import json
from typing import cast
from datetime import date
from urllib3 import HTTPResponse

KEY = '2w4sI8BiTXK6sKcw9rp6Q5P_qeLVNQGp'
client = RESTClient(api_key=KEY)

aggs = cast(
    HTTPResponse,
    client.get_aggs('AAPL', 1, 'day', '2023-01-01', '2023-02-01', raw=True),)

data = json.loads(aggs.data)
print(data)
