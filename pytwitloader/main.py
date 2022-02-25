import json
from pprint import pprint
import re
import logging
import os
import string
import sys

import downloader
import twitter_calls
from configuration import config

logger = logging.getLogger("main")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("output.log")
formatter = logging.Formatter("%(levelname)s:%(name)s:%(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Gifs are stored as mp4s on twitter
FILETYPES = {"photo": "jpg", "video": "mp4", "animated_gif": "mp4"}

TESTING = 1  # limit number of files parsed

def sanitize_text(text):
    # Cursed url regex, do not look
    text = re.sub(
        "(?:(?:(https:){0,1}\/\/))([\w_-]+(?:(?:\.[\w_-]+)+))(?:([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]){0,1})",
        "",
        text,
    )
    text = text.rstrip()
    text = text.replace(".", "")
    text = text.replace(".", "")
    text = re.sub('[/\\.:*?<>"|]', "", text)
    return text


def get_filename(index, type, text, screen_name):
    text = sanitize_text(text)
    extension = FILETYPES[type]
    if index:
        filename = f"{screen_name}_{text}_{index}.{extension}"
    else:
        filename = f"{screen_name}_{text}.{extension}"
    filename = filename.replace("\n", " ")
    filename = f'{config["DOWNLOAD_DIRECTORY"]}/{filename}'
    if len(filename) > 50:
        print(filename)
        filename = filename[:50]
    return filename


def parse_page(liked_page):
    for tweet in liked_page:
        if "extended_entities" in tweet:
            try:
                media_list = tweet["extended_entities"]["media"]
                for index, media in enumerate(media_list):
                    # print(len(media))
                    filename = get_filename(
                        index + 1 if len(media_list) > 1 else None,
                        media["type"],
                        tweet["text"],
                        tweet["user"]["screen_name"],
                    )
                    if media["type"] == "photo":
                        downloader.download_image(media["media_url_https"], filename)
                    if media["type"] == "video":
                        downloader.download_video(
                            media["video_info"]["variants"][-1]["url"], filename
                        )
                    if media["type"] == "animated_gif":
                        downloader.download_video(
                            media["video_info"]["variants"][-1]["url"], filename
                        )
            except KeyError:
                # logger.error(json.dumps(tweet, indent=4, sort_keys=True))
                logger.error(f"Some error with parsing tweet: {tweet['text']}")


def main():
    tweet_count = 0
    max_id = None
    while True:
        # TODO: Rewrite this as a generator
        liked_page = twitter_calls.get_liked_tweets(max_id)
        if not liked_page:
            break
        parse_page(liked_page)
        max_id = (
            liked_page[-1]["id"] - 1
        )  # Need to use -1 because passing previous id as is returns that tweet
        tweet_count += len(liked_page)
    print(f"Processed {tweet_count} tweets")


if __name__ == "__main__":
    # input_text = "Maison Margiela Fall 2016 RTW https://t.co/BZSMUGZYeU"
    # print(get_filename(None, input_text, None))
    main()
