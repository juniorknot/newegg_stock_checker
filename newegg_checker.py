
import requests
import browser_cookie
import sys
import time
from bs4 import BeautifulSoup

from pushbullet import PushBullet

monitor_list = [
    #'https://www.newegg.ca/Product/Product.aspx?Item=9SIA7RD5UG3951&cm_re=rx_580-_-9SIA7RD5UG3951-_-Product',
    #'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814137117&cm_re=rx_580-_-14-137-117-_-Product',
    #'https://www.newegg.ca/Product/Product.aspx?Item=9SIA7BB5VA5029&cm_re=rx_580-_-14-137-120-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814125964&cm_re=rx_580-_-14-125-964-_-Product'
]

pushbulley_key_file = "pushbullet.key"

s = requests.session()
s.headers.update({'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'})
time.sleep(3)

# pushbullet
with open(pushbulley_key_file, "r") as file:
    pushbullet_key = file.readline().strip()
pb = PushBullet(pushbullet_key)

while True:
    for url in monitor_list:
        r = s.get(url)
        if r.status_code == 200:
            data = r.text
            soup = BeautifulSoup(data, "html.parser")

            # check seller
            seller = ""
            seller_divs = soup.find_all("div", {"class": "seller"})
            print seller_divs
            if seller_divs != None and seller_divs != []:
                seller = seller_divs[0].a.string
                print seller
            else:
                seller_divs = soup.find_all("div", {"class": "featured-seller"})
                if seller_divs != None and seller_divs != []:
                    seller = seller_divs[0].div.strong.string
                    print seller
            if seller == "":
                print "seller error"

            print soup.prettify()
            cart_div = soup.find(id="landingpage-cart")

            print cart_div.string
            print cart_div.childern

            time.sleep(10)
        print ""



    sys.exit()



