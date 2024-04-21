from pydantic import BaseModel

from src.categories import Category


class News(BaseModel):
    text: str
    link: str
    categories: set[Category] | None = None
    jaccard_index: float | None = None
