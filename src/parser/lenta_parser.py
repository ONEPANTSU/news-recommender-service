import requests
from bs4 import BeautifulSoup

from src.dto import News
from src.parser.base_parser import BaseParser


class LentaParser(BaseParser):
    _BASE_URL = "https://lenta.ru"
    _SEARCH_URL = f"{_BASE_URL}/parts/news/"

    def _get_news_from_page(self, page) -> list[News]:
        response = requests.get(self._SEARCH_URL + str(page))
        soup = BeautifulSoup(response.content, "html.parser")
        news_elements = soup.find_all("a", class_="_parts-news")

        news = []
        for news_element in news_elements:
            title = news_element.find(
                "h3", class_="card-full-news__title"
            ).text
            link = news_element["href"]
            news.append(News(text=title, link=self._BASE_URL + link))

        return news
