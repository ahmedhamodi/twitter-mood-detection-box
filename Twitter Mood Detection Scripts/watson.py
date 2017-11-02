import json
import requests

text = "This is a test"
features = {"entities": {}, "emotion": {}, "keywords": {}}
version = '2017-02-27'
username = '7caf2a5f-b43f-4179-bcaf-48c639026d99'
password = 'x715aBvw1aYC'
base_url = 'https://gateway.watsonplatform.net'
url = '/natural-language-understanding/api/v1/models'
headers = {'content-type': 'application/json', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}
params = {'version': '2017-02-27'}
data = {"clean": True, "features": features, "fallback_to_raw": True, "text": text, "return_analyzed_text": False}

response = requests.request(method="POST", url=base_url + url, auth=(username, password), headers=headers, params=params, data=data).json()

print(json.dumps(response, indent=2))

