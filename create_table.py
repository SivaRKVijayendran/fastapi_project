from database import Base, engine
from model import Book
from sqlalchemy import inspect


print("DB URL : " , engine.url)
inspection = inspect(engine)
print("fastapi_db tables before : " , inspection.get_table_names())

Base.metadata.create_all(bind=engine)
inspection = inspect(engine)
print("fastapi_db tables after : " , inspection.get_table_names())