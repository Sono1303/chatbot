from tool.clean_data import clean_data
from tool.modified_data import modified_data
from tool.modified_data_image import modified_data_image
from tool.modified_data_2 import modified_data_2
import time

def preprocessing_data(data_input, data_output=None, saved_image_folder=None,  modified = 0, modified_2 = 0, clean = 0, modified_image = 0):
    try:
        if modified == 1:
            modified_data(data_input, data_output)

        time.sleep(1)
        if clean == 1 and modified == 1:
            clean_data(data_output)
        elif clean == 1:
            clean_data(data_input)

        if modified_2 == 1 and modified == 1:
            modified_data_2(data_output)
        elif modified_2 == 1:
            modified_data_2(data_input)

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
    preprocessing_data(OUTPUT_PATH, None, IMAGE_PATH, 0, 0, 0, 1)