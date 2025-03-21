import json 
import os

JSON_PATH = r"E:\Chatbot\Neural_network_chatbot\data\intents.json"

def modified_data_image(data_input, saved_image_folder):
    data = json.load(open(data_input))

    modified_data = []
    for item in data['intents']:
        image_path = saved_image_folder + "\\" + item['tag'] + ".jpg"
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

    with open(data_input, 'w') as f:
        json.dump(modified_json, f, indent=4)

    print("Done modified image!")