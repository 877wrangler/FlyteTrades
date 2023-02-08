from polygon.rest import RESTClient
import json, config
from typing import cast
from datetime import date
from urllib3 import HTTPResponse

import config

client = RESTClient(api_key=config.POLYGON_KEY)

aggs = cast(
    HTTPResponse,
    client.get_aggs('AAPL', 1, 'day', '2023-01-01', '2023-02-01', raw=True),)

data = json.loads(aggs.data)
print(data)
