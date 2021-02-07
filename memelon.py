from time import sleep
from pyrh import Robinhood
from dotenv import load_dotenv
import os
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, timedelta
import urllib.request
from imageai.Detection.Custom import CustomObjectDetection
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

load_dotenv()

doge_words = ["doge", "such wow", "much wow", "dogecoin"]
execution_path = os.getcwd()
temp_path = os.path.join(execution_path, "temp")
models_path = os.path.join(execution_path, "doge-training/doge-identification/models/")

rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))
rh.login()


def check_if_image_contains_doge(image_path):
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, os.path.join(models_path + "doge-detection.h5")))
    detector.setJsonPath(os.path.join(execution_path, "doge-training/doge-identification/json/detection_config.json"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=image_path, minimum_percentage_probability=80,
                                                 output_image_path=image_path)
    if len(detections) != 0:
        buy_doge()


def check_for_doge_in_tweet_text(tweet_text):
    tweet_text = tweet_text.lower()
    if any(substring in tweet_text for substring in doge_words):
        print("Tweet talking about doge: ", tweet_text)
        buy_doge()
        return True
    return False


def check_for_new_tweet():
    print("checking_for_new_tweet")
    # auth = OAuthHandler(os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
    # auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    # auth_api = API(auth)
    #
    # elon = auth_api.get_user("elonmusk")
    #
    # end_date = datetime.utcnow() - timedelta(days=4)
    # for status in Cursor(auth_api.user_timeline, id=elon.id, exclude_replies=True, include_retweets=False).items():
    #     if status.created_at < end_date:
    #         break
    #     if check_for_doge_in_tweet_text(status.text):
    #         break
    #     if hasattr(status, "entities"):
    #         entities = status.entities
    #         if "media" in entities:
    #             media_arr = entities["media"]
    #             for media in media_arr:
    #                 if media["type"] == "photo":
    #                     filename = media["media_url"].split('/')[-1]
    #                     image_path = os.path.join(temp_path, filename)
    #                     urllib.request.urlretrieve(media["media_url"], image_path)
    #                     check_if_image_contains_doge(image_path)
    #                     os.remove(image_path)


def check_doge_for_increase(buy_price):
    current_price = float(rh.get_crypto_quote("1ef78e1b-049b-4f12-90e5-555dcf2fe204")["mark_price"])
    difference = ((current_price - buy_price)/buy_price) * 100

    if float(difference) >= float(10):
        print("selling doge for: ", current_price)
        sold = True
        # rh.place_market_crypto_sell_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)


def buy_doge():
    print("Attempting to buy DogeCoin")
    # request = rh.place_market_crypto_buy_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)
    # if request.status_code == 200:
    #     print("Bought DogeCoin")
    # else:
    #     print("Failed to buy DogeCoin: ", request.message)
    doge_price = float(rh.get_crypto_quote("1ef78e1b-049b-4f12-90e5-555dcf2fe204")["mark_price"])
    # rt = RepeatedTimer(2, check_doge_for_increase, 0.050)


def run():
    print("running application")


def main():
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    load_dotenv()

    logging.basicConfig(level=logging.DEBUG)
    try:
        with BlockingScheduler() as scheduler:
            scheduler.add_schedule(run(), IntervalTrigger(seconds=1))
    except (KeyboardInterrupt, SystemExit):
        pass


main()
