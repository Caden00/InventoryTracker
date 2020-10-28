# This will handle parsing and returning useable json data.

import requests
import pprint
import json
import selenium
import pyppeteer

from selenium import webdriver

# Variables / Constants

product_page = 'https://www.bestbuy.com/site/playstation-5/ps5-consoles/pcmcat1587395025973.c?id=pcmcat1587395025973'

# Parameters to access website
params = 

# Chromium Driver
# I am using this to test the links being created from parsing
# driver = webdriver.Chrome('/Users/cadenaragon/Documents/GitHub/InventoryTracker/chromedriver')

# opening up the main page for the PS5
# driver.get(product_page)

# Return the json format for the page
json_info = requests.get(product_page)

pprint.pprint(json_info)