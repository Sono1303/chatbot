import json 

def clean_data(data_input):
    data = json.load(open(data_input))

    exist_tag = []
    cleaned_data = []
    deleted_data = []
    
    for item in data['intents']:
        if item['tag'] not in  exist_tag:
            if type(item['tag']) is tuple:
                exist_tag.append(item['tag'][0])
            exist_tag.append(item['tag'])
            cleaned_data.append(item)
        else:
            deleted_data.append(item['tag'])
            del item

    print("Before clean:", len(data['intents']))
    print("After clean:", len(cleaned_data))
    
    cleaned_json = {
        "intents": cleaned_data
    }

    with open(data_input, 'w') as f:
        json.dump(cleaned_json, f, indent=4)

    print(deleted_data)
    print("Done clean data")
