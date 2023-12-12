import requests
import jinja2

x = requests.get('https://api.justjoin.it/v2/user-panel/offers?categories[]=3&page=1&sortBy=published&orderBy=DESC&perPage=100&salaryCurrencies=PLN')
print(x.status_code)
