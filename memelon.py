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

load_dotenv()
app_scheduler = BlockingScheduler()
rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))

doge_words = ["doge", "such wow", "much wow", "dogecoin", "Ðogecoin", "Ð"]
execution_path = os.getcwd()
temp_path = os.path.join(execution_path, "temp")
models_path = os.path.join(execution_path, "doge-training/doge-identification/models/")


def image_contains_doge(image_path):
    detector = CustomObjectDetection()
    detector.setModelTypeAsYOLOv3()
    detector.setModelPath(os.path.join(execution_path, os.path.join(models_path + "doge-detection.h5")))
    detector.setJsonPath(os.path.join(execution_path, "doge-training/doge-identification/json/detection_config.json"))
    detector.loadModel()
    detections = detector.detectObjectsFromImage(input_image=image_path, minimum_percentage_probability=80,
                                                 output_image_path=image_path)
    if len(detections) != 0:
        pause_tweet_job()
        add_buy_doge_job()
        return True
    return False


def check_for_doge_in_tweet_text(tweet_text):
    tweet_text = tweet_text.lower()
    if any(substring in tweet_text for substring in doge_words):
        pause_tweet_job()
        add_buy_doge_job()
        return True
    return False


def check_for_new_tweet(auth_api):
    elon = auth_api.get_user("elonmusk")

    end_date = datetime.utcnow() - timedelta(minutes=1)
    for status in Cursor(auth_api.user_timeline, id=elon.id, exclude_replies=True, include_retweets=False).items():
        if status.created_at < end_date:
            return
        if check_for_doge_in_tweet_text(status.text):
            print("Tweet contains doge: ", status.text)
            return
        if hasattr(status, "entities"):
            entities = status.entities
            if "media" in entities:
                media_arr = entities["media"]
                for media in media_arr:
                    if media["type"] == "photo":
                        filename = media["media_url"].split('/')[-1]
                        image_path = os.path.join(temp_path, filename)
                        urllib.request.urlretrieve(media["media_url"], image_path)
                        contains_doge = image_contains_doge(image_path)
                        os.remove(image_path)
                        if contains_doge:
                            print("Tweet contains doge: ", status.text)
                            return


def sell_doge_after_increase(buy_price, starting_time):
    if not rh.authenticated:
        rh.login()
    current_price = float(rh.get_crypto_quote("1ef78e1b-049b-4f12-90e5-555dcf2fe204")["mark_price"])
    difference = ((current_price - buy_price)/buy_price) * 100

    if float(difference) >= float(10):
        print("selling doge for: ", current_price, " and profiting ", str(current_price - buy_price), " per DogeCoin")
        rh.place_market_crypto_sell_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", float(os.getenv("AMOUNT_TO_SPEND")))
        app_scheduler.remove_job("sell_doge_on_increase")
        resume_tweet_job()
    end_date = datetime.utcnow() - timedelta(minutes=60)
    if starting_time < end_date:
        print("Doge did not increase enough, cancelling sell order and going back to watching tweets")
        app_scheduler.remove_job("sell_doge_on_increase")
        resume_tweet_job()


# Robinhoods order date seems to be an hour off so i am just checking the order time
def check_doge_buy_order(order_id, order_time):
    if not rh.authenticated:
        rh.login()
    order_status = rh.get_crypto_orders(order_id)[0]
    if order_status["state"] == "filled":
        print("Bought DogeCoin at: ", order_status["price"])
        app_scheduler.remove_job("check_doge_order")
        add_sell_doge_job(float(order_status["price"]))

    end_date = datetime.utcnow() - timedelta(minutes=10)
    if order_time < end_date:
        cancel_request = rh.cancel_crypto_order(order_status["cancel_url"])
        if not cancel_request:
            print("Cancelled Doge order as it was not filled in time")
            app_scheduler.remove_job("check_doge_order")
            resume_tweet_job()


def buy_doge():
    if not rh.authenticated:
        rh.login()
    request = rh.place_market_crypto_buy_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", float(os.getenv("AMOUNT_TO_SPEND")))
    res = request.json()
    if request.status_code == 201:
        print("Attempting to buy DogeCoin at: ", res["price"])
        add_check_doge_order_job(res["id"])
    else:
        print("Failed to place DogeCoin Buy Order: ", res)
        resume_tweet_job()


def add_buy_doge_job():
    app_scheduler.add_job(buy_doge, id="buy_doge")


def add_sell_doge_job(doge_price):
    print("Added sell order job... waiting for price to increase.")
    app_scheduler.add_job(sell_doge_after_increase, IntervalTrigger(seconds=int(os.getenv("DOGE_PRICE_PULL_INTERVAL"))),
                          args=[doge_price, datetime.now()], id="sell_doge_on_increase")


def add_check_doge_order_job(order_id):
    app_scheduler.add_job(check_doge_buy_order, IntervalTrigger(seconds=10), args=[order_id, datetime.now()],
                          id="check_doge_order")


def add_tweet_job():
    auth = OAuthHandler(os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
    auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
    auth_api = API(auth)
    print("Waiting for elon to tweet...")
    app_scheduler.add_job(check_for_new_tweet, IntervalTrigger(seconds=int(os.getenv("TWEET_PULL_INTERVAL"))),
                          args=[auth_api], id="check_tweets")


def pause_tweet_job():
    app_scheduler.pause_job("check_tweets")


def resume_tweet_job():
    print("Waiting for elon to tweet...")
    app_scheduler.resume_job("check_tweets")


def main():
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

    add_tweet_job()
    print("Starting Memelon")
    try:
        app_scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        app_scheduler.shutdown()
        pass


main()
