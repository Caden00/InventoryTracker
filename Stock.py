# This will handle parsing page data
import requests
import pprint
from bs4 import BeautifulSoup

# Variables / Constants

product_page = 'https://www.bestbuy.com/site/apple-20w-usb-c-power-adapter-white/6437121.p?skuId=6437121'
a = 'https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149'

request_headers = {
    'authority': 'www.bestbuy.com',
    'pragma': 'no-cache',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36' \
                  ' (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
    'accept': '*/*',
    'sec-fetch-site': 'same-orgin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.bestbuy.com/site/apple-3-3-usb-type-a-to-lightning-charging-cable-white/6259806.p?skuId=6259806',
    'accept-language': 'en-US,en;q=0.9'
}

# Return the json format for the page
page_request = requests.get(product_page, headers=request_headers)

# Return request status
print(page_request.status_code)

parse_html = BeautifulSoup(page_request.content, 'html.parser')

check_add_to_cart = parse_html.find("div", {"class": "fulfillment-add-to-cart-button"})

button = parse_html.find('button', {'class': 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'})

if button is not None:
    print('Item is in stock')





