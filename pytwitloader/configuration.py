import logging
import sys
import json
import os

logger = logging.getLogger("main")

config = None


def get_twitter_keys():
    config = {}
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, "r") as config_file:
            config = json.load(config_file)
    else:
        env_vars = os.environ
        try:
            config["TWITTER_CONSUMER_KEY"] = env_vars["TWITTER_CONSUMER_KEY"]
            config["TWITTER_CONSUMER_SECRET"] = env_vars["TWITTER_CONSUMER_SECRET"]
            config["TWITTER_ACCESS_KEY"] = env_vars["TWITTER_ACCESS_KEY"]
            config["TWITTER_ACCESS_SECRET"] = env_vars["TWITTER_ACCESS_SECRET"]
        except KeyError:
            logger.exception(
                "No config file passed, and no environment variables found"
            )
            sys.exit()
    return config


config = get_twitter_keys()
