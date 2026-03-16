from sqlalchemy import inspect
from auth.auth_database import Base , engine
import auth.auth_model

print("DB URL : " , engine.url)
inspection = inspect(engine)
print("fastapi_db tables before : " , inspection.get_table_names())

Base.metadata.create_all(bind=engine)
inspection = inspect(engine)
print("fastapi_db tables after : " , inspection.get_table_names())