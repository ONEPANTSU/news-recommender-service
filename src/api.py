from fastapi import FastAPI, Query

from src.agent import Agent
from src.parser.parsers import Parsers

app = FastAPI(prefix="/agent")
agent = Agent()


@app.get("/{parser}/", tags=["agent"])
async def get_news(
        parser: Parsers = Parsers.LENTA,
        categories: list[str] = Query(default=None),
) -> list[dict[str, str]]:
    return await agent.get_news(categories=categories, parser=parser)
