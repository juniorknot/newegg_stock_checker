
import requests
import sys
import time
#from bs4 import BeautifulSoup

#from pushbullet import PushBullet
import telegram

monitor_list = [
    '9SIA7BB5V53526',
    'N82E16814202278',
    'N82E16814137120',
    'N82E16814131719',
    'N82E16814131713',
    'N82E16814137135',
    'N82E16814125962',
    'N82E16814202279',
    'N82E16814125964',
    'N82E16814126192',
    'N82E16814202277',
    'N82E16814137117',
    'N82E16814137119'
]

#pushbulley_key_file = "pushbullet.key"
telegram_key_file = "telegram.key"

s = requests.session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.2'})

web_url_base = "https://www.newegg.ca/Product/Product.aspx?Item="
api_url_base = "http://www.ows.newegg.ca/Products.egg/"

time.sleep(3)

'''
# pushbullet
with open(pushbulley_key_file, "r") as file:
    pushbullet_key = file.readline().strip()
pb = PushBullet(pushbullet_key)
'''

# telegram
with open(telegram_key_file, "r") as file:
    telegram_token = file.readline().strip()
    telegram_chat_id = file.readline().strip()
telegram_bot = telegram.Bot(token=telegram_token)


while True:
    for item in monitor_list:
        r = s.get(api_url_base + item)
        data = None
        if r.status_code == 200:
            data = r.json()

        final_price = 999
        can_buy = False
        if data and isinstance(data, dict):
            final_price = float(data['Basic']['FinalPrice'][1:])
            if data['Basic']['AddToCartText'] == 'Add To Cart':
                can_buy = True
            print final_price
            print can_buy

        if final_price < 400 and can_buy:
            #pb.push_link("newegg", web_url_base + item)
            telegram_bot.send_message(chat_id=telegram_chat_id, text=web_url_base+item)

        time.sleep(10)

    time.sleep(30)




