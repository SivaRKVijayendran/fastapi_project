
from pydantic import BaseModel

class Book(BaseModel):
    id : int
    title : str
    author : str
    publish_date : str


class Book_update(BaseModel):
    title : str
    author : str
    publish_date : str