import grpc

from src.categories import Categories
from src.config import CLASSIFIER_HOST, CLASSIFIER_PORT
from src.dto import News
from src.parser.lenta_parser import LentaParser
from src.parser.parsers import Parsers
from src.rpc import *


class RecommenderService:
    def __init__(self):
        self.__classifier_addr = f"{CLASSIFIER_HOST}:{CLASSIFIER_PORT}"
        self.parsers = {
            Parsers.LENTA: LentaParser(),
        }

    async def get_news(
        self, categories: set[Categories], parser: Parsers = Parsers.LENTA
    ):
        all_news = self.parsers[parser].get_news()
        if categories:
            news = []
            for news_info in all_news:
                news_info.categories = await self.__classify_news(
                    news_info.text
                )
                news_info.jaccard_index = self.__get_jaccard_index(
                    categories, news_info.categories
                )
                if news_info.jaccard_index > 0:
                    news.append(news_info)
            all_news = self.__sort_news_by_jaccard(news)
        return all_news

    async def __classify_news(self, text: str) -> set[Categories]:
        async with grpc.aio.insecure_channel(
            self.__classifier_addr
        ) as channel:
            stub = classifier_pb2_grpc.NewsClassifierStub(channel)
            response: classifier_pb2.NewsClassificationReply = (
                await stub.ClassifyNews(
                    classifier_pb2.NewsClassificationRequest(text=text)
                )
            )
        return set(response.categories)

    @staticmethod
    def __get_jaccard_index(
        preferred_categories: set[str], news_categories: set[str]
    ) -> float:
        intersection = len(preferred_categories.intersection(news_categories))
        union = len(preferred_categories.union(news_categories))
        return 0 if union == 0 else intersection / union

    @staticmethod
    def __sort_news_by_jaccard(news: list[News]) -> list[News]:
        return sorted(news, key=lambda x: x.jaccard_index, reverse=True)
