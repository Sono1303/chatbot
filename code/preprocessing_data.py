from tool.clean_data import clean_data
from tool.modified_data import modified_data
from tool.modified_data_image import modified_data_image
import time
def preprocessing_data(data_input, data_output=None, saved_image_folder=None,  modified = 0, clean = 0, modified_image = 0):
    try:
        if modified == 1:
            modified_data(data_input, data_output)

        time.sleep(1)
        if clean == 1 and modified == 1:
            clean_data(data_output)
        elif clean == 1:
            clean_data(data_input)

        time.sleep(1)
        if modified_image == 1 and modified == 1:
            modified_data_image(data_output, saved_image_folder)
        elif modified_image == 1:
            modified_data_image(data_input, saved_image_folder)
    except Exception as e:
        print(e)
    
    print("Done preprocessing")
    
INPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\ing.json'
OUTPUT_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'
IMAGE_PATH = r'E:\Chatbot\Neural_network_chatbot\images'

if __name__ == '__main__':
    preprocessing_data(INPUT_PATH, OUTPUT_PATH, IMAGE_PATH, 1, 1, 1)