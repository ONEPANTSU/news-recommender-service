import grpc

from src.categories import Categories
from src.config import CLASSIFIER_HOST, CLASSIFIER_PORT
from src.parser.lenta_parser import LentaParser
from src.parser.parsers import Parsers
from src.rpc import *


class Agent:
    def __init__(self):
        self.classifier_api = f"{CLASSIFIER_HOST}:{CLASSIFIER_PORT}"
        self.parsers = {
            Parsers.LENTA: LentaParser(),
        }

    async def get_news(
            self,
            categories: list[Categories],
            parser: Parsers = Parsers.LENTA
    ):
        all_news = self.parsers.get(parser, "Parser not found").get_news()
        if categories is not None:
            news = []
            for news_item in all_news:
                news_categories = await self.__classify_news(news_item["title"])
                if all(category in news_categories for category in categories):
                    news.append(news_item)
            return news
        else:
            return all_news

    async def __classify_news(self, text: str) -> list[str]:
        async with grpc.aio.insecure_channel(self.classifier_api) as channel:
            stub = classifier_pb2_grpc.NewsClassifierStub(channel)
            response: classifier_pb2.NewsClassificationReply = await stub.ClassifyNews(
                classifier_pb2.NewsClassificationRequest(text=text)
            )
        return response.categories
