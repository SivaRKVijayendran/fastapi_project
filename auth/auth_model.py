from sqlalchemy import  Column , Integer , VARCHAR , String
from auth_database import Base

class User(Base):

    __tablename__ = "users"

    id = Column(Integer , primary_key= True , index= True)
    username =  Column(String(250) , unique=True , index=True )
    email = Column(String(250) , unique=True , index=True)
    hashed_password = Column(String(250))
    role = Column(String(250) , default="user")

