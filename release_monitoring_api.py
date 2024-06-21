import json

import requests

# https://release-monitoring.org/project/201/

# https://release-monitoring.org/static/docs/api.html#get--api-project-(int-project_id)
response = requests.get(url="https://release-monitoring.org/api/project/201")
json_dict = json.loads(response.content)
# pprint(json_dict.keys())
print(json_dict["name"])

# https://release-monitoring.org/static/docs/api.html#get--api-v2-versions-
response = requests.get(url="https://release-monitoring.org/api/v2/versions/", params={"project_id": 201})
json_dict = json.loads(response.content)
# pprint(json_dict.keys())
print(json_dict["latest_version"])
