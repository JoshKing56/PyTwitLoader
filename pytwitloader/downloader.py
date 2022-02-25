import requests
import shutil
import logging

logger = logging.getLogger("main")

def download_image(url, filename):
    res = requests.get(url, stream = True)
    
    if res.status_code == 200:
            with open(filename,'wb') as f:
                shutil.copyfileobj(res.raw, f) 

    else:
        logger.DEBUG('Could not download: {filename} Url: {url}')
    print(f"Downloading: {url}")

def download_video(url, filename):
    r = requests.get(url, stream = True) 

    # download started 
    with open(filename, 'wb') as f: 
        for chunk in r.iter_content(chunk_size = 1024*1024): 
            if chunk: 
                f.write(chunk) 
    print(f"Downloading: {url}")