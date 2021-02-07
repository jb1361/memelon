from pyrh import Robinhood
from dotenv import load_dotenv
import os
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
from datetime import datetime, date, time, timedelta
from collections import Counter
import sys

load_dotenv()

auth = OAuthHandler(os.getenv("TWITTER_CONSUMER_KEY"), os.getenv("TWITTER_CONSUMER_SECRET"))
auth.set_access_token(os.getenv("TWITTER_ACCESS_TOKEN"), os.getenv("TWITTER_ACCESS_TOKEN_SECRET"))
auth_api = API(auth)

elon = auth_api.get_user("elonmusk")

end_date = datetime.utcnow() - timedelta(days=2)
for status in Cursor(auth_api.user_timeline, id=elon.id, exclude_replies=True, include_retweets=False).items():
    print(status)
    if hasattr(status, "entities"):
        entities = status.entities
    if status.created_at < end_date:
        break

# rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))
# rh.login()
# print(rh.get_account())
# rh.place_market_crypto_sell_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)
