import json
import requests

text = input()
features = {"emotion": {}}
version = '2017-02-27'
username = '7caf2a5f-b43f-4179-bcaf-48c639026d99'
password = 'x715aBvw1aYC'
base_url = 'https://gateway.watsonplatform.net'
url = '/natural-language-understanding/api/v1/analyze'
headers = {'content-type': 'application/json', 'accept': 'application/json', 'user-agent': 'watson-developer-cloud-python-0.26.1'}
params = {'version': '2017-02-27'}
data = json.dumps({"clean": True, "features": features, "fallback_to_raw": True, "text": text, "return_analyzed_text": False})

response = requests.Request(method="POST", url=base_url + url, auth=(username, password), headers=headers, params=params, data=data)

def pretty_print_POST(req):
    """
    At this point it is completely built and ready
    to be fired; it is "prepared".

    However pay attention at the formatting used in 
    this function because it is programmed to be pretty 
    printed and may differ from the actual request.
    """
    print('{}\n{}\n{}\n\n{}'.format(
        '-----------START-----------',
        req.method + ' ' + req.url,
        '\n'.join('{}: {}'.format(k, v) for k, v in req.headers.items()),
        req.body,
    ))

pretty_print_POST(response.prepare())

\

