from time import sleep
from pyrh import Robinhood
from dotenv import load_dotenv
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, timedelta
import urllib.request
import os
# disable tensorflow debug information
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from imageai.Detection.Custom import CustomObjectDetection
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging

load_dotenv()
app_scheduler = BlockingScheduler()
rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))

doge_words = ["doge", "such wow", "much wow", "dogecoin"]
execution_path = os.getcwd()
temp_path = os.path.join(execution_path, "temp")
models_path = os.path.join(execution_path, "doge-training/doge-identification/models/")


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
        add_buy_doge_job()
        pause_tweet_job()
        return True
    return False


def check_for_new_tweet(auth_api):
    elon = auth_api.get_user("elonmusk")

    end_date = datetime.utcnow() - timedelta(days=4)
    for status in Cursor(auth_api.user_timeline, id=elon.id, exclude_replies=True, include_retweets=False).items():
        if status.created_at < end_date:
            break
        if check_for_doge_in_tweet_text(status.text):
            break
        if hasattr(status, "entities"):
            entities = status.entities
            if "media" in entities:
                media_arr = entities["media"]
                for media in media_arr:
                    if media["type"] == "photo":
                        filename = media["media_url"].split('/')[-1]
                        image_path = os.path.join(temp_path, filename)
                        urllib.request.urlretrieve(media["media_url"], image_path)
                        check_if_image_contains_doge(image_path)
                        os.remove(image_path)


def check_doge_for_increase(buy_price, rh):
    current_price = float(rh.get_crypto_quote("1ef78e1b-049b-4f12-90e5-555dcf2fe204")["mark_price"])
    difference = ((current_price - buy_price)/buy_price) * 100

    if float(difference) >= float(10):
        print("selling doge for: ", current_price)
        # rh.place_market_crypto_sell_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)
        app_scheduler.remove_job("sell_doge_on_increase")
        print(app_scheduler.get_jobs())
        resume_tweet_job()
        print(app_scheduler.get_jobs())


def buy_doge():
    print("Attempting to buy DogeCoin")
    # request = rh.place_market_crypto_buy_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)
    # if request.status_code == 200:
    #     print("Bought DogeCoin")
    # else:
    #     print("Failed to buy DogeCoin: ", request.message)
    doge_price = float(rh.get_crypto_quote("1ef78e1b-049b-4f12-90e5-555dcf2fe204")["mark_price"])
    print("First: ", app_scheduler.get_jobs())
    pause_tweet_job()


def login_to_robinhood():
    global rh
    rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))
    rh.login()


def add_buy_doge_job():
    app_scheduler.add_job(buy_doge, id="buy_doge")


def add_sell_doge_job(doge_price):
    app_scheduler.add_job(check_doge_for_increase, IntervalTrigger(seconds=3), args=[doge_price, rh],
                          id="sell_doge_on_increase")


def add_tweet_job():
    auth = OAuthHandler(os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    auth_api = API(auth)
    app_scheduler.add_job(check_for_new_tweet, IntervalTrigger(seconds=20), args=[auth_api], id="check_tweets")


def pause_tweet_job():
    app_scheduler.pause_job("check_tweets")


def resume_tweet_job():
    app_scheduler.resume_job("check_tweets")


def main():
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    add_tweet_job()
    print("initial: ", app_scheduler.get_jobs())
    try:
        app_scheduler.start()
        print("test: ", app_scheduler.get_jobs())
    except (KeyboardInterrupt, SystemExit):
        app_scheduler.shutdown()
        pass


main()
