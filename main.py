import requests
import json
import matplotlib.pyplot as plt
import collections

def save_to_json_file(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4)

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

# EXTRACT - create offers jsons
offers = []
for key,value in categories.items():
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
    
num_of_all_offers = len(offers)
offers = list(filter(lambda offer: offer['employmentTypes'][0]['to'] is not None, offers))
num_of_offers_with_salary = len(offers)

print(f"In justjoin.it there are {num_of_all_offers} offers.")
print(f"Of which {num_of_offers_with_salary} offers have salary.")
print(f"That is {num_of_offers_with_salary/num_of_all_offers:.0%}.")
    
save_to_json_file(offers, "offers.json")
    
# TANSFORM - convert jsons into a dataframe ready for Pandas or Matplotlib
skills = []
for offer in offers:
    salary = offer['employmentTypes'][0]
    for req_skill in offer['requiredSkills']:
        skills.append({'name': req_skill, 'categoryId': offer['categoryId'], 'salary_from':salary['from'], 'salary_to':salary['to']})

print(f'{len(skills)} instances of skills saved.')
save_to_json_file(skills, "skills.json")
skills_counts = collections.Counter(s['name'] for s in skills)
print(f'There are {len(skills_counts)} unique skills.')
