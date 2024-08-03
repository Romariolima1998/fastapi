from typing import Union, List
from pydantic import BaseModel, Field, HttpUrl


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title='te description the item', max_length=300)
    price: float = Field(
        gt=0, description='the price must be greater than zero')
    tax: Union[float, None] = None
    tags: list[str] = []
    image: Image | None = None


class User(BaseModel):
    username: str
