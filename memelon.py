from pyrh import Robinhood
from dotenv import load_dotenv
import os

load_dotenv()

rh = Robinhood(username=os.getenv("RH_USERNAME"), password=os.getenv("RH_PASSWORD"))
rh.login()
print(rh.get_account())
#rh.place_market_crypto_sell_order("1ef78e1b-049b-4f12-90e5-555dcf2fe204", 1.00)