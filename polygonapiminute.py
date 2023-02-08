import datetime, time
from polygon.rest import RESTClient
import json, config
from typing import cast
from datetime import date, datetime
from urllib3 import HTTPResponse

# Delayed data
today = datetime.now().date()
start_time = datetime.strptime("9:45 AM", "%I:%M %p").time()
start_bar = datetime.combine(today, start_time)
end_time = datetime.strptime("10:00 AM", "%I:%M %p").time()
end_bar = datetime.combine(today, start_time)
print(start_bar)
client = RESTClient(api_key=config.POLYGON_KEY)


aggs = cast(
    HTTPResponse,
    client.get_aggs('AAPL', 1, 'minute', start_bar, end_bar, raw=True),)

data = json.loads(aggs.data)
print(data)


