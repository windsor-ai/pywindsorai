# pywindsorai

`pywindsorai` is a python package makes it easy to get marketing data from any platform like facebook, google ads, bing into python.

[Windsor.ai](https://www.windsor.ai/) allows to get marketing data from any platform. It beautifully simplifies the complexity of dealing with multiple platforms, unlocking unified, valuable information in a format that matters to you. For more details checkout [onboard.windsor.ai](https://onboard.windsor.ai/).

## Features

✅ Easy access to marketing data via windsor.ai APIs

✅ Lightweight (single dependency - [requests](https://pypi.org/project/requests/))

✅ Supports both python 2.7+ and 3

## Usage

### Installation

```sh
pip install pywindsorai
```

### Registration

You need to get a free API key to access windsor.ai's APIs. Register your account first and add a datasource like facebook ads and then get the API key. For more details check out our official [API documentation](https://www.windsor.ai/api-documentation/) and [this article](https://www.windsor.ai/api-fields/). Get the API key at https://onboard.windsor.ai 

### Minimal Example

```python
from pywindsorai.client import Client
from pywindsorai.enums import LAST_7D
from pywindsorai.enums import FIELD_SOURCE, FIELD_CAMPAIGN, FIELD_CLICKS

api_key = 'xxx'  # Get it from your windsor.ai account. It's recommended to store and get this securely, for example an env variable.

# Setup a client object with the API key
client = Client(api_key)

# Call the /connectors API.
campaign_clicks = client.connectors(date_preset=LAST_7D, fields=[FIELD_SOURCE, FIELD_CAMPAIGN, FIELD_CLICKS])

# can also be run like:
campaign_clicks = client.connectors(date_preset='last_7d', fields=['date','clicks','spend'])

# Response will be a python dict (parsed from the json response recieved).
print(campaign_clicks)

[
  {'date': '2021-04-15', 'clicks': 3, 'spend': 8.139999999999999},
  {'date': '2021-04-15', 'clicks': 2, 'spend': 6.51},
  {'date': '2021-04-15', 'clicks': 1, 'spend': 3.88},
  {'date': '2021-04-15', 'clicks': 4, 'spend': 3.275311},
  {'date': '2021-04-15', 'clicks': 6, 'spend': 1.408321}],

```
