import json 

data = json.load(open('intents.json'))

exist_tag = []
cleaned_data = []
for item in data['intents']:
    if item['tag'] not in  exist_tag:
        if type(item['tag']) is tuple:
            exist_tag.append(item['tag'][0])
        exist_tag.append(item['tag'])
        cleaned_data.append(item)
    else:
        del item

print(len(data['intents']))
print(len(cleaned_data))

cleaned_json = {
    "intents": cleaned_data
}

with open('intents.json', 'w') as f:
    json.dump(cleaned_json, f, indent=4)