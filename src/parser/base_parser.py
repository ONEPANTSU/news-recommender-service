from abc import ABC, abstractmethod

from src.dto import News


class BaseParser(ABC):
    _BASE_URL: str
    _SEARCH_URL: str

    def get_news(self, page_offset=1, news_limit=100) -> list[News]:
        current_page = page_offset
        news = []
        try:
            while len(news) < news_limit:
                news.extend(self._get_news_from_page(current_page))
                current_page += 1
        except Exception as exception:
            print(str(exception))

        return news[:news_limit]

    @abstractmethod
    def _get_news_from_page(self, page) -> list[News]:
        pass
