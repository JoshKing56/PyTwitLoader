import logging
import sys
import json
import os

logger = logging.getLogger("main")
config = None

VARIABLES_LIST = ["TARGET_USER", "DOWNLOAD_DIRECTORY", "TWITTER_BEARER_TOKEN"]

def get_twitter_keys():
    config = {}
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        with open(filename, "r") as config_file:
            config = json.load(config_file)
    else:
        try:
            for env_var in VARIABLES_LIST:
                config[env_var] = os.environ[env_var]
        except KeyError:
            logger.exception(
                "No config file passed, and no environment variables found"
            )
            sys.exit()
    return config


config = get_twitter_keys()
