import os
import time
import json
import urllib.request
import json

JSON_PATH = r'E:\Chatbot\Neural_network_chatbot\data\intents.json'
SAVE_DIR = r'E:\Chatbot\Neural_network_chatbot\images'
# API_KEY = "AIzaSyB0B1sdPRSehthxM8h9kL7wWFJD8EOR5RI"
API_KEY = "AIzaSyAFjIA4_3q79BbVWmlWPUJLRCIRlcMXDUg"
CX = "b61b39304c482409a"

def download_images(data):
    def download_image(input):
        search_term = input.replace(" ", "%20") 

        save_dir = SAVE_DIR
        os.makedirs(save_dir, exist_ok=True)

        def fetch_image_urls(query, num_images=1):
            image_urls = []
            for start in range(0, num_images, 10):  
                url = (
                    f"https://www.googleapis.com/customsearch/v1?q={query}"
                    f"&cx={CX}&searchType=image&num=10&start={start+1}&key={API_KEY}"
                )
                try:
                    response = urllib.request.urlopen(url)
                    data = json.load(response)
                    items = data.get("items", [])
                    for item in items:
                        image_urls.append(item.get("link"))
                except Exception as e:
                    print(f"Error fetching images: {e}")
                time.sleep(1)  # Avoid rate limiting
            return image_urls

        def download_images(image_urls):
            for idx, img_url in enumerate(image_urls):
                try:
                    print(f"Downloading {img_url} ...")
                    img_path = os.path.join(save_dir, f"{search_term}.jpg")
                    urllib.request.urlretrieve(img_url, img_path)
                    break
                except Exception as e:
                    print(f"Failed to download {img_url}: {e}")

        image_urls = fetch_image_urls(search_term, num_images=15)
        download_images(image_urls)
    # print("Download complete!")

    with open(data) as f:
        data = json.load(f)

    for item in data['intents'][5:]:
        if not item['tag'].startswith('recipe'):
            download_image(item["tag"])

if __name__ == '__main__':
    download_images(JSON_PATH)