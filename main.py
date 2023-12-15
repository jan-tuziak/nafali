import requests
import jinja2
import json

headers = {'Version': '2'}
x = requests.get('https://api.justjoin.it/v2/user-panel/offers?&page=1&sortBy=published&orderBy=DESC&perPage=100', headers=headers)
offers = json.dumps(x.json(), indent=4)
with open("offers.json", "w") as outfile:
    outfile.write(offers)
