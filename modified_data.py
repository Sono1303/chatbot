import json 
import os

JSON_PATH = r"E:\Chatbot\Neural_network_chatbot\data\intents.json"

data = json.load(open(JSON_PATH))

modified_data = []
for item in data['intents']:
    image_path = "E:/Chatbot/Neural_network_chatbot/images/" + item['tag'] + ".jpg"
    # print(image_path)
    # print(os.path.isfile(image_path))
    if os.path.isfile(image_path):
        tmp = item
        tmp['image'] = image_path
        # print(tmp)
        modified_data.append(tmp)
    else:
        modified_data.append(item)
    
modified_json = {
    "intents": modified_data
}

with open(JSON_PATH, 'w') as f:
    json.dump(modified_json, f, indent=4)