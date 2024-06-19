import requests
import json
import matplotlib.pyplot as plt
import collections
import os

delta = 100 #PLN

def save_to_json_file(data, filename):
    with open(filename, "w") as outfile:
        json.dump(data, outfile, indent=4)

def load_from_json_file(filename):
    with open(filename) as f:
        return json.load(f)
    
def create_hist_data(og_offers, categoryId = -1, skills = None):
    offers = og_offers.copy()
    if (categoryId != -1):
        offers = [o for o in offers if o['categoryId'] == categoryId]
    
    if (skills is not None):
        for skill in skills:
            offers = [o for o in offers if skill in o['requiredSkills']]

    data = []
    for o in offers:
        start = int(o['employmentTypes'][0]['from_pln'])
        stop = int(o['employmentTypes'][0]['to_pln']) + 1
        data.extend(list(range(start, stop, delta)))
    return data

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
if os.path.exists('offers.json'):
    offers = load_from_json_file("offers.json")
else:
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
    save_to_json_file(offers, "offers.json")
    
num_of_all_offers = len(offers)
offers = list(filter(lambda offer: offer['employmentTypes'][0]['to'] is not None, offers))
num_of_offers_with_salary = len(offers)

print(f"In justjoin.it there are {num_of_all_offers} offers.")
print(f"Of which {num_of_offers_with_salary} offers have salary.")
print(f"That is {num_of_offers_with_salary/num_of_all_offers:.0%}.")

## filter offers for over 20k PLN net
offers = list(filter(lambda offer: int(offer['employmentTypes'][0]['from_pln']) > 20000, offers))
print(f"In justjoin.it there are {len(offers)} offers with salary >20k PLN net.")

# barchart for categories
# category_counts_20k = collections.Counter(o['categoryId'] for o in offers)
# print(category_counts_20k)
# categories_20k = []
# data_20k = []
# for k,v in category_counts_20k.items():
#     categories_20k.append(categories[str(k)])
#     data_20k.append(v)
# fig, ax = plt.subplots()
# ax.bar(categories_20k, data_20k)


# # TANSFORM - convert jsons into a dataframe ready for Pandas or Matplotlib
# skills = []
# for offer in offers:
#     salary = offer['employmentTypes'][0]
#     for req_skill in offer['requiredSkills']:
#         skills.append({'name': req_skill, 'categoryId': offer['categoryId'], 'salary_from':salary['from'], 'salary_to':salary['to']})

# print(f'{len(skills)} instances of skills saved.')
# save_to_json_file(skills, "skills.json")
# skills_counts = collections.Counter(s['name'] for s in skills)
# print(f'There are {len(skills_counts)} unique skills.')
# popular_skills = {k: v for k, v in skills_counts.items() if v > 20}
# print(popular_skills)
# print(len(skills_counts))
# print(len(popular_skills))

# for k,v in popular_skills.items():
#     popular_skills[k] = list(filter(lambda offer: k in offer['requiredSkills'], offers))

# for k,v in popular_skills.items():
#     popular_skills[k] = []
#     for offer in v:
#         start = int(offer['employmentTypes'][0]['from_pln'])
#         stop = int(offer['employmentTypes'][0]['to_pln']) + 1
#         delta = 1000 #PLN
#         data = list(range(start, stop, delta))
#         popular_skills[k].extend(data)

# data = []
# labels = []
# for k,v in  popular_skills.items():
#     data.append(v)
#     labels.append(k)

# fig = plt.figure()
# ax = fig.add_subplot(111)

# bp = ax.boxplot(data, patch_artist = True, notch ='True')

# ax.set_xticklabels(labels)
# ax.get_yaxis().tick_left()
# ax.get_xaxis().tick_bottom()
# ax.tick_params(axis='x', labelrotation=90)
# plt.show()

# plt.hist(create_hist_data(offers, -1, ['Machine Learning']), delta, alpha=0.5, label='ML')

## .NET Breakdown
# plt.hist(create_hist_data(offers, 7, ['Angular']), delta, alpha=0.5, label='.NET + Angular')

## MOBILE breakdown
# plt.hist(create_hist_data(offers, 10), delta, alpha=0.5, label='Mobile')
# plt.hist(create_hist_data(offers, 10, ['Swift']), delta, alpha=0.5, label='Swift')
# plt.hist(create_hist_data(offers, 10, ['Kotlin']), delta, alpha=0.5, label='Kotlin')
# plt.hist(create_hist_data(offers, 10, ['Java']), delta, alpha=0.5, label='Java')
# plt.hist(create_hist_data(offers, 10, ['Flutter']), delta, alpha=0.5, label='Flutter')
# plt.hist(create_hist_data(offers, 10, ['Android']), delta, alpha=0.5, label='Android')
# plt.hist(create_hist_data(offers, 10, ['iOS']), delta, alpha=0.5, label='iOS')

## DEVOPS breakdown
# plt.hist(create_hist_data(offers, 12), delta, alpha=0.5, label='devops')
# plt.hist(create_hist_data(offers, 12, ['Azure']), delta, alpha=0.5, label='DevOps - Azure')
# plt.hist(create_hist_data(offers, 12, ['GCP']), delta, alpha=0.5, label='DevOps - GCP')
# plt.hist(create_hist_data(offers, 12, ['AWS']), delta, alpha=0.5, label='DevOps - AWS')

## TESTING breakdown
# plt.hist(create_hist_data(offers, 11), delta, alpha=0.5, label='Testing')
# plt.hist(create_hist_data(offers, 11, ['Selenium']), delta, alpha=0.5, label='Testing - Selenium')
# plt.hist(create_hist_data(offers, 11, ['Playwright']), delta, alpha=0.5, label='Testing - Playwright')
# plt.hist(create_hist_data(offers, 11, ['Java']), delta, alpha=0.5, label='Testing - Java')
# plt.hist(create_hist_data(offers, 11, ['Python']), delta, alpha=0.5, label='Testing - Python')
# plt.hist(create_hist_data(offers, 11, ['JavaScript']), delta, alpha=0.5, label='Testing - JavaScript')
# plt.hist(create_hist_data(offers, 11, ['C#']), delta, alpha=0.5, label='Testing - C#')

## WINNERS
# plt.hist(create_hist_data(offers, 12), delta, alpha=0.5, label='devops')
# plt.hist(create_hist_data(offers, 19), delta, alpha=0.5, label='data')
# plt.hist(create_hist_data(offers, 20), delta, alpha=0.5, label='Go')
# plt.hist(create_hist_data(offers, 8), delta, alpha=0.5, label='Scala')
# plt.hist(create_hist_data(offers, 6), delta, alpha=0.5, label='Java')
# plt.hist(create_hist_data(offers, 5), delta, alpha=0.5, label='python')
# plt.hist(create_hist_data(offers, 18), delta, alpha=0.5, label='security')


### LOSERS
# plt.hist(create_hist_data(offers, 24), delta, alpha=0.5, label='other')
# plt.hist(create_hist_data(offers, 22), delta, alpha=0.5, label='erp')
# plt.hist(create_hist_data(offers, 23), delta, alpha=0.5, label='Arch')
# plt.hist(create_hist_data(offers, 13), delta, alpha=0.5, label='Admin')
# plt.hist(create_hist_data(offers, 9), delta, alpha=0.5, label='C')
# plt.hist(create_hist_data(offers, 4), delta, alpha=0.5, label='ruby')
# plt.hist(create_hist_data(offers, 10), delta, alpha=0.5, label='Mobile')
# plt.hist(create_hist_data(offers, 1, ['Angular']), delta, alpha=0.5, label='Angular in JS category')
# plt.hist(create_hist_data(offers, 7), delta, alpha=0.5, label='.NET')
# plt.hist(create_hist_data(offers, 11), delta, alpha=0.5, label='Testing')
# plt.hist(create_hist_data(offers, 1), delta, alpha=0.5, label='javascript')

plt.hist(create_hist_data(offers, 12), delta, alpha=0.5, label='devops')
plt.hist(create_hist_data(offers, 5), delta, alpha=0.5, label='python')
plt.hist(create_hist_data(offers, 20), delta, alpha=0.5, label='Go')
plt.hist(create_hist_data(offers, -1, ['Machine Learning']), delta, alpha=0.5, label='ML')

plt.legend(loc='upper right')
plt.show()