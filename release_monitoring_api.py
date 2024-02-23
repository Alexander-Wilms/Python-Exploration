import json
from pprint import pprint

import requests

# https://release-monitoring.org/static/docs/api.html#get--api-v2-versions-
URL = "https://release-monitoring.org/api/v2/versions/"

# https://release-monitoring.org/project/201/
response = requests.get(url=URL, params={"project_id": 201})

json_dict = json.loads(response.content)
pprint(json_dict.keys())
print(json_dict["latest_version"])
