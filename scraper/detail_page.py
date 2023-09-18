import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
import time
import json

SELECTORS = {
    'full_descr_btn': '//a[@id="full_descr_block_bt"]',
    'price_filter_btn': '//a[contains(text(), "ціні")]',
    'store_rows': '//tr[contains(@class,"list")]',
    '_shop_name': './td[contains(@class, "shoplogo")]/a',
    '_shop_price': './td[contains(@class, "price")]',
}


class DetailPage(webdriver.Chrome):
    def __init__(self, url: str, *args, **kwargs):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        super(DetailPage, self).__init__(options=options, *args, **kwargs)
        self.url = url
        self.details_data = {}

    def get_page(self):
        self.get(self.url)
        self.implicitly_wait(10)

    def get_price_page(self):
        self.get(self.url.replace('desc', 'pric'))
        self.implicitly_wait(10)

    def get_details(self):
        data = {}
        try:
            full_descr_btn = self.find_element(By.XPATH, SELECTORS['full_descr_btn'])
            full_descr_btn.click()
        except NoSuchElementException:
            pass
        table = self.find_element(By.ID, 'help_table')

        # Iterate through the rows in the table
        for row in table.find_elements(By.TAG_NAME, 'tr'):
            cells = row.find_elements(By.TAG_NAME, 'td')
            if len(cells) == 2:
                key = cells[0].text.strip().replace('\n','')
                value = cells[1].text.strip().replace('\n','')
                data[key] = value


        return data

    def get_price(self):
        shops = []
        try:
            full_descr_btn = self.find_element(By.XPATH, SELECTORS['price_filter_btn'])
            full_descr_btn.click()
        except NoSuchElementException:
            pass
        try:
            for row in self.find_elements(By.XPATH, SELECTORS['store_rows']):
                shop_name = row.find_element(By.XPATH, SELECTORS['_shop_name']).get_attribute('title')
                shop_price = row.find_element(By.XPATH, SELECTORS['_shop_price']).text
                shop = {'name': shop_name, 'price': shop_price}
                shops.append(shop)
            return shops
        except NoSuchElementException as e:
            print(e)
