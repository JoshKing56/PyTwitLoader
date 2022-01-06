import requests
import shutil
import logging

logger = logging.getLogger("main")

def download_image(url, filename):
    # res = requests.get(url, stream = True)
    
    # if res.status_code == 200:
    #     with open(filename,'wb') as f:
    #         shutil.copyfileobj(res.raw, f) 
    # else:
    #     logger.DEBUG('Could not download: {filename} Url: {url}')
    print(f"Downloading: {filename}")

def download_video(url, filename):
    print(f"Downloading: {filename}")