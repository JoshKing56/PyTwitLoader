import logging
import sys
import json
import requests

from configuration import config

logger = logging.getLogger("main")

def get_liked_tweets(max_id = None): 
    url = "https://api.twitter.com/1.1/favorites/list.json"
    
    headers = {
    'Authorization': f'Bearer {config["TWITTER_BEARER_TOKEN"]}',
    }

    parameters = {
        'screen_name': config["TARGET_USER"],
        'count': 200
    }
    if max_id:
        parameters['max_id'] = max_id
    
    response = requests.request("GET", url, headers=headers, params=parameters)
    logger.debug(f"Request: {url}, response: {response.status_code}")
    if response.status_code != 200:
        logger.exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
        sys.exit()
    return(response.json())