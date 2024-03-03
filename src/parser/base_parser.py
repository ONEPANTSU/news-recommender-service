import logging

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from src.config import SELENIUM_HOST, SELENIUM_PORT
from src.product import *


class Parser:
    def __init__(self):
        options = Options()
        options.add_argument("--disable-infobars")
        options.add_argument("start-maximized")
        options.add_argument("--disable-extensions")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        )
        options.add_experimental_option(
            "prefs", {"profile.default_content_setting_values.notifications": 1}
        )
        self.driver = webdriver.Remote(
            options=options,
            command_executor=f"http://{SELENIUM_HOST}:{SELENIUM_PORT}",
        )
        self.product_maker = ProductMaker()

    def get_products(self, category: str, start_page=1, page_limit=100):
        current_page = start_page
        last_page = start_page + page_limit - 1
        products = []
        try:
            while current_page <= last_page:
                self.driver.get(
                    "https://megamarket.ru/catalog/"
                    + category
                    + "/page-"
                    + str(current_page)
                )
                self.confirm_city()
                products_from_page = self.get_products_from_page()
                products.extend(products_from_page)
                current_page += 1
        except Exception as exception:
            print(str(exception))

        return products

    def __del__(self):
        self.driver.quit()

    def get_products_from_page(
        self,
    ):
        products = []
        products_info = self.driver.find_elements(By.CLASS_NAME, "item-info")
        for index in range(len(products_info)):
            if (
                products_info[index].text == "Купить"
                or products_info[index + 1].text != "Купить"
            ):
                continue
            info_list = products_info[index].text.split("\n")
            link = None
            try:
                link = (
                    products_info[index]
                    .find_elements(By.CLASS_NAME, "ddl_product_link")[0]
                    .get_attribute("href")
                )
            except IndexError:
                print(f"Failed to get link for {products_info[index].text}")
            info_list.append(link)
            product = self.product_maker.get_product(info_list)
            products.append(product)
        return products

    def confirm_city(self):
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            if button.text == "Да":
                button.click()
                break


def get_max_bonus(products: BonusProduct):
    products = [product for product in products if isinstance(product, BonusProduct)]
    return max(products, key=lambda x: x.bonus)


def get_max_bonus_percent(products: BonusProduct):
    products = [product for product in products if isinstance(product, BonusProduct)]
    return max(products, key=lambda x: x.bonus_percent)


def get_sorted_by_bonus(products: BonusProduct):
    products = [product for product in products if isinstance(product, BonusProduct)]
    return sorted(products, key=lambda x: x.bonus, reverse=True)


def get_sorted_by_bonus_percent(products: BonusProduct, list_length: int = 3):
    products = [product for product in products if isinstance(product, BonusProduct)]
    return sorted(products, key=lambda x: x.bonus_percent, reverse=True)[:list_length]
