from pydantic import BaseModel

from src.categories import Categories


class News(BaseModel):
    text: str
    link: str
    categories: set[Categories] | None = None
    jaccard_index: float | None = None
