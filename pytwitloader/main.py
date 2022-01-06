import json
import logging
import os
import sys

import tweepy

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('output.log')
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def get_twitter_keys():
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, "r") as config_file:
            config = json.load(config_file)
        return config["consumer_key"], config["consumer_secret"]
    else:
        env_vars = os.environ
        try:
            return env_vars["TWITTER_CONSUMER_KEY"], env_vars["TWITTER_CONSUMER_SECRET"]
        except KeyError:
            logger.error("No config file passed, and no environment variables found") 
            # print("testing")
            sys.exit()


def main():
    consumer_key, consumer_secret = get_twitter_keys()
    print(f"Key: {consumer_key},\nSecret :{consumer_secret}")
    # auth = tweepy.OAuthHandler(config["tw"], consumer_secret)
    # token = session.get('request_token')
    # session.delete('request_token')
    # auth.request_token = { 'oauth_token' : token,
    #                         'oauth_token_secret' : verifier }


    # try:
    #     auth.get_access_token(verifier)
    # except tweepy.TweepError:
    #     print('Error! Failed to get access token.')


if __name__ == "__main__":
    main()

