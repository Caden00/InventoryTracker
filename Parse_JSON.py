# This will handle parsing and returning useable json data.

import requests
import pprint
import json
import selenium
import pyppeteer

from selenium import webdriver

# Variables / Constants

product_page = 'https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973'

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

# Chromium Driver
# I am using this to test the links being created from parsing
# driver = webdriver.Chrome('/Users/cadenaragon/Documents/GitHub/InventoryTracker/chromedriver')

# opening up the main page for the PS5
# driver.get(product_page)

# Return the json format for the page
json_info = requests.get(product_page, headers=request_headers)

pprint.pprint(json_info)