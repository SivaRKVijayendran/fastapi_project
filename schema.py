from pydantic import BaseModel, ConfigDict


class Bookstore(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

    model_config = ConfigDict(from_attributes=True)

class Book_update(BaseModel):
    title: str
    author: str
    publish_date: str

    model_config = ConfigDict(from_attributes=True)