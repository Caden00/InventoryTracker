# This will handle parsing page data
import requests
import pprint
from bs4 import BeautifulSoup
import time

# Variables / Constants

product_page = 'https://www.bestbuy.com/site/nvidia-geforce-rtx-3080-10gb-gddr6x-pci-express-4-0-graphics-card-titanium-and-black/6429440.p?skuId=6429440'
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

class Check_Stock:
    # Constructor
    def __init__(self, product_page, headers):
        self.product_page = product_page
        self.headers = headers
        # Constant request page
        self.page_request = requests.get(product_page, headers=request_headers)


    # Get the page request status (Should be 200)
    def request_status(self):
        return self.page_request.status_code

    # Will check for item availability
    def stock(self):
        # Get the html code
        parse_html = BeautifulSoup(self.page_request.content, 'html.parser')
        # Check the button for adding to cart
        button = parse_html.find('button', {'class': 'btn btn-primary btn-lg btn-block btn-leading-ficon add-to-cart-button'})
        # Return true or false based on stock
        if button is not None:
            # print('Item is in stock')
            return True
        else:
            # print('Out of Stock')
            return False
