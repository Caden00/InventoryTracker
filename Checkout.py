# When the item come into stock, this will be used to checkout
# This will use a webbrower to navigate through the checkout process

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.select import Select

class Checkout:
    def __init__(self, product_page, headers, personal_info):
        self.product_page = product_page
        self.headers = headers
        self.driver = webdriver.Chrome(r'C:\Users\Caden Aragon\Documents\GitHub\InventoryTracker\chromedriver.exe')
        self.personal_info = personal_info


    def pass_keys(self):
        self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.firstName').send_keys(personal_info['first_name'])
        self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.lastName').send_keys(personal_info['last_name'])
        self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.street').send_keys(personal_info['address'])
        self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.zipcode').send_keys(personal_info['zip_code'])
        self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.city').send_keys(personal_info['city'])
        self.driver.find_element_by_id('user.emailAddress').send_keys(personal_info['email'])
        self.driver.find_element_by_id('user.phone').send_keys(personal_info['phone_number'])

        select = Select(self.driver.find_element_by_id('consolidatedAddresses.ui_address_2.state'))

        select.select_by_visible_text('CO')


    def navigate(self):
        # Open webpage
        self.driver.get(self.product_page)
        time.sleep(1)
        # Find the add to cart button
        self.driver.find_element_by_class_name('fulfillment-add-to-cart-button').click()
        # Go to checkout
        self.driver.get('https://www.bestbuy.com/cart')

        time.sleep(2)
        # Hit checkout button and checkout as guest
        self.driver.find_element_by_class_name(r'checkout-buttons__checkout').click()
        time.sleep(2)
        self.driver.find_element_by_class_name(r'button-wrap').click()

        time.sleep(2)

        if self.driver.find_element_by_class_name('ispu-card__switch').text != 'Switch to Shipping':
            self.pass_keys()
        else:
            self.driver.find_element_by_class_name('ispu-card__switch').click()
            time.sleep(2)
            self.pass_keys()



product_page = 'https://www.bestbuy.com/site/apple-magsafe-iphone-charger-white/6341029.p?skuId=6341029'

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

personal_info = {
    'first_name': 'Caden',
    'last_name': 'Aragon',
    'email': 'cadenaragon@gmail.com',
    'address': '123 some st.',
    'city': 'Colorado Springs',
    'state': 'CO',
    'zip_code': '80920',
    'phone_number': '0123456789'
}

test = Checkout(product_page, request_headers, personal_info)

test.navigate()
