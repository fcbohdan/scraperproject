from scraper.detail_page import DetailPage
from scraper.result_page import ResultPage
import pandas as pd
from datetime import datetime
import click
import json


BRANDS = {
    'apple': '116',
    'samsung': '147',
    'huawei': '647',
    'xiaomi': '3917',
    'sony': '156',
    'lg': '102',
    'nokia': '120',
    'motorola': '112',
    'htc': '736',
    'asus': '190',
    'alcatel': '8',
    'google': '1364',
}


def is_valid_price(ctx, param, value):
    if value < 0:
        raise click.BadParameter('Price must be positive')
    return value


@click.command()
@click.option("--max_price",
              "-t",
              type=int,
              default=125000,
              callback=is_valid_price,
              help="Max price for the item",
              )
@click.option("--min_price",
              "-f",
              type=int,
              default=0,
              callback=is_valid_price,
              help="Min price for the item",
              )
@click.option("--brand",
              "-b",
              type=click.Choice(BRANDS.keys(), case_sensitive=True),
              help="Brand name. LOWERCASE ONLY",
              )
def cli(
        max_price: int,
        min_price: int,
        brand: str = None,
):
    result_page = ResultPage()
    page = 0
    if brand:
        url = f"https://m.ua/ua/m1_magazilla.php?katalog_=122&page_={page}&minPrice_={min_price}&maxPrice_={max_price}&brands_={BRANDS[brand]}"
    else:
        url = f"https://m.ua/ua/m1_magazilla.php?katalog_=122&page_={page}&minPrice_={min_price}&maxPrice_={max_price}"
    result_page.create_items_csv_if_not_exist()
    result_page.get_page(url)
    print("getting first result page")
    result_page.get_list_items()
    result_page.list_items_to_csv()
    list_of_pages = result_page.get_pages_list()
    result_page.quit()
    if 1 in list_of_pages:
        for page_nr in list_of_pages:
            print("getting next result page")
            if brand:
                url = f"https://m.ua/ua/m1_magazilla.php?katalog_=122&page_={page_nr}&minPrice_={min_price}&maxPrice_={max_price}&brands_={BRANDS[brand]}"
            else:
                url = f"https://m.ua/ua/m1_magazilla.php?katalog_=122&page_={page_nr}&minPrice_={min_price}&maxPrice_={max_price}"
            result_page = ResultPage()
            result_page.get_page(url)
            result_page.get_list_items()
            result_page.list_items_to_csv()
    df = pd.read_csv('items.csv')
    for index, row in df.iterrows():
        url = row['url']
        spider = DetailPage(url)
        spider.get_page()
        details = spider.get_details()
        spider.get_price_page()
        pricelist = spider.get_price()
        data = {
            'name': row['name'],
            'url': row['url'],
            'price': row['price'],
            'details': details,
            'pricelist': pricelist
        }
        filename = f"output/{datetime.now().strftime('%Y-%m-%d')}_{row['name'].lower().replace(' ','_')}.json"
        try:
            with open(filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            print(f"Data saved to {filename} successfully.")
        except Exception as e:
            print(f"An error occurred while saving to {filename}: {e}")
        spider.quit()


if __name__ == "__main__":
    cli()
