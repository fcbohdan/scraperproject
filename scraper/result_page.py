import re
import os

import pandas as pd
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

SELECTORS = {
    'nr_items': '//td[@class="num-models"]/div',
    'item_rows': '//tr[contains(@class,"list")]',
    '_item_price': './/div//span[contains(text(), "грн")]',
    '_item_name': './/div[@class="list-model-title"]/a',
}


class ResultPage(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        super(ResultPage, self).__init__(options=options, *args, **kwargs)
        self.items = []

    def get_page(self, url):
        self.get(url)
        self.implicitly_wait(10)

    def get_pages_list(self):
        """
        :return:
            list of pages numbers where items are listed
        """
        nr_items_raw = self.find_element(By.XPATH, SELECTORS['nr_items']).text
        pattern = "Вибрано (?P<nr_items>\d+) моделей:"
        match = re.search(pattern=pattern, string=nr_items_raw)
        if match:
            nr_items = int(match['nr_items'])
        pages = [n + 1 for n in range(nr_items // 15)]
        if nr_items // 24 == 0:
            pages = [0]
        return pages

    def get_list_items(self):
        try:
            for row in self.find_elements(By.XPATH, SELECTORS['item_rows']):
                item_name = row.find_element(By.XPATH, SELECTORS['_item_name']).text
                item_url = row.find_element(By.XPATH, SELECTORS['_item_name']).get_attribute('href')
                item_price = row.find_element(By.XPATH, SELECTORS['_item_price']).get_attribute('innerHTML')
                item = {'name': item_name, 'url': item_url, 'price': item_price}
                self.items.append(item)
        except NoSuchElementException as e:
            print(e)

    def create_items_csv_if_not_exist(self):
        # Check if the file exists
        if not os.path.isfile('items.csv'):
            # If the file doesn't exist, create it and write the header
            with open('items.csv', 'w') as file:
                file.write("name,url,price\n")
            print("File 'items.csv' has been created with the header.")

    def list_items_to_csv(self):
        df = pd.DataFrame(self.items)
        df['price'] = df['price'].str.replace('грн', '')
        df['price'] = df['price'].str.replace('&nbsp;', '')
        df['price'] = df['price'].str.replace('.', '')
        df.to_csv('items.csv', index=False, mode='a', header=False)
