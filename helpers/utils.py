import json

with open('json_data.json') as json_file:
    titles = json.load(json_file)

for title in titles:
    print(title)