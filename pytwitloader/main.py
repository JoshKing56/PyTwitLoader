import json
import logging
import os
import sys
import configuration
# import tweepy
import requests

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("output.log")
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    config = configuration.get_twitter_keys()
    bearer_token = config["TWITTER_BEARER_TOKEN"]
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    # r.headers["User-Agent"] = "v2LikedTweetsPython"
    return r

def main():
    id = "1094960355384745985"
    url = f"https://api.twitter.com/2/users/{id}/liked_tweets" 
    # tweet_fields = "tweet.fields=lang,author_id"
    response = requests.request("GET", url, auth=bearer_oauth)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    # print(response.json)
    print(json.dumps(response.json(), indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
