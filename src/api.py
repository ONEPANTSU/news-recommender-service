from fastapi import FastAPI, Query

from src.categories import Categories
from src.dto import News
from src.parser.parsers import Parsers
from src.service import RecommenderService


class RecommenderAPI(FastAPI):
    def __init__(self):
        super().__init__(prefix="/recommender_api")
        self.service = RecommenderService()
        self.add_api_route(
            methods=["GET"],
            path="/get_recommendations",
            endpoint=self.get_news,
            tags=["News Recommendations"],
        )

    async def get_news(
        self,
        parser: Parsers,
        categories: set[Categories] = Query(default_factory=set),
    ) -> list[News]:
        return await self.service.get_news(
            categories=set(categories), parser=parser
        )


app = RecommenderAPI()
