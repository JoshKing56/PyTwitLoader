import json
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

TESTING = 1 # limit number of files parsed

def get_filename(index, type, text, screen_name):
    text = text.rsplit(" ", 1)[0] # last "word" in text is always the twitter url. remove this.
    extension = FILETYPES[type]
    filename = f"{screen_name} | {text} | {index}.{extension}"
    filename = filename.replace("\n", " ")
    return filename

def parse_page(liked_page):
    for tweet in liked_page:
        if "extended_entities" in tweet:
            try:
                media_list = tweet["extended_entities"]["media"]
                for index, media in enumerate(media_list):
                    filename = get_filename(
                        index + 1,
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
        max_id = liked_page[-1]["id"] - 1 #Need to use -1 because passing previous id as is returns that tweet
        tweet_count += len(liked_page)
    print(f"Processed {tweet_count} tweets") 
    

    
if __name__ == "__main__":
    # input_text = "Maison Margiela Fall 2016 RTW https://t.co/BZSMUGZYeU"
    # print(get_filename(None, input_text, None))
    main()
