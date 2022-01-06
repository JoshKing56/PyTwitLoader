import json
import logging
import os
import sys

import twitter_calls
from configuration import config

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("output.log")
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def main():
    liked_page = twitter_calls.get_liked_tweets()
    print(json.dumps(liked_page[0], indent=4, sort_keys=True))

if __name__ == "__main__":
    main()
