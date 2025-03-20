import json 

def modified_data(data_input, data_output):
    data = json.load(open(data_input))
    # print(data)
    modified_data = []
    for item in data:
        pattern = []
        dish = item['dish']
        response = f'With ingredients, you can make {dish} \n'
        for i in item['ingredients']:
            pattern.append(i['name'])
            name, quantity = i['name'], i['quantity']
            response += f'- {name}: {quantity} \n'
        modified_data.append(
            {
                'tag': item['tag'],
                'patterns': pattern,
                'responses': response,
                'context_set': ''
            }
        )
        
    modified_json = {
        "intents": modified_data
    }

    with open(data_output, 'w') as f:
        json.dump(modified_json, f, indent=4)
    
    print("Done modified data")

INPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\ing.json'
OUTPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'

if __name__ == '__main__':
    modified_data(INPUT_PATH, OUTPUT_PATH)