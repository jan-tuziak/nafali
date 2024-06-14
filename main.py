import requests
import json
import os

categories = {
    "1": "JavaScript",
    "2": "HTML",
    "3": "PHP",
    "4": "Ruby",
    "5": "Python",
    "6": "Java",
    "7": ".NET",
    "8": "Scala",
    "9": "C",
    "10": "Mobile",
    "11": "Testing",
    "12": "DevOps",
    "13": "Admin",
    "14": "UX-UI",
    "15": "PM",
    "16": "Game",
    "17": "Analytics",
    "18": "Security",
    "19": "Data",
    "20": "Go",
    "21": "Support",
    "22": "ERP",
    "23": "Architecture",
    "24": "Other"
}

for key,value in categories.items():
    # EXTRACT - create offers jsons
    offers = []
    headers = {'Version': '2'}
    page = 1
    x = requests.get(f'https://api.justjoin.it/v2/user-panel/offers?categories[]={key}&page=1&sortBy=published&orderBy=DESC&perPage=100', headers=headers)
    assert x.status_code == 200, f"Status Code should be 200, but is {x.status_code}"
    x = x.json()
    while page <= x['meta']['totalPages']:
        x = requests.get(f'https://api.justjoin.it/v2/user-panel/offers?categories[]={key}&page={page}&sortBy=published&orderBy=DESC&perPage=100', headers=headers)
        assert x.status_code == 200, f"Status Code should be 200, but is {x.status_code}"
        x =x.json()
        page = x['meta']['page'] + 1
        offers = offers + x['data']
        
    filename = f"offers/{value}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as outfile:
        offers_json = json.dump(offers, outfile, indent=4)
    
    # LOAD - convert jsons into a csv ready for Pandas or Matplotlib



