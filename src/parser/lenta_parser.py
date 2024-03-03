from src.parser.base_parser import BaseParser


class FontankaParser(BaseParser):
    URL = "https://www.fontanka.ru/"
    def get_news_from_page(self) -> list[str]:
        pass