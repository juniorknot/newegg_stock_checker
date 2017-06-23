
import requests
import dryscrape
import webkit_server
#import browser_cookie
import sys
import time
from bs4 import BeautifulSoup

from pushbullet import PushBullet

monitor_list = [
    'https://www.newegg.ca/Product/Product.aspx?Item=9SIA7BB5VA5029&cm_re=rx_580-_-14-137-120-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814131719&cm_re=rx_580-_-14-131-719-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814131713&cm_re=rx_580-_-14-131-713-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814125962&cm_re=rx_580-_-14-125-962-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814126192&cm_re=rx_580-_-14-126-192-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=9SIA7RD5UG3380&cm_re=rx_580-_-14-126-196-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=9SIA93K5VS4580&cm_re=rx_580-_-9SIA93K5VS4580-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814137135&cm_re=rx_580-_-14-137-135-_-Product',
    'https://www.newegg.ca/Product/Product.aspx?Item=N82E16814125964&cm_re=rx_580-_-14-125-964-_-Product'
]

pushbulley_key_file = "pushbullet.key"

s = dryscrape.Session()
s.set_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0')
time.sleep(3)

# pushbullet
with open(pushbulley_key_file, "r") as file:
    pushbullet_key = file.readline().strip()
pb = PushBullet(pushbullet_key)

while True:
    for url in monitor_list:
        try:
            s.visit(url)
            data = s.body()

        except webkit_server.InvalidResponseError:
            continue
        soup = BeautifulSoup(data, "html.parser")

        # check seller
        seller = ""
        seller_divs = soup.find_all("div", {"class": "seller"})
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

        can_buy = False
        cart_div = soup.find(id="landingpage-cart")
        if cart_div != None:
            if "ADD TO CART" in cart_div.prettify():
                can_buy = True
                print "can buy"
            else:
                print "not available"
        else:
            print "cart error"

        if seller.strip() == "Newegg" and can_buy:
            pb.push_link("newegg", url)

        time.sleep(10)

    time.sleep(30)




