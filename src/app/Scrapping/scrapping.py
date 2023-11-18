import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    with open(save_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=128):
            file.write(chunk)

def scrape_images(url, save_directory):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    img_tags = soup.find_all('img')
    for img_tag in img_tags:
        img_url = urljoin(url, img_tag['src'])
        img_name = os.path.basename(img_url)
        img_path = os.path.join(save_directory, img_name)

        download_image(img_url, img_path)