from fastapi import FastAPI, Query

from src.categories import Category
from src.dto import News
from src.parser.parser_type import ParserType
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
        parser: ParserType,
        categories: set[Category] = Query(default_factory=set),
    ) -> list[News]:
        return await self.service.get_news(
            categories=categories, parser=parser
        )


app = RecommenderAPI()
