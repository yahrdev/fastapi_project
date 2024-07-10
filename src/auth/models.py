"""The User model"""

from sqlalchemy import Integer

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy.orm import  Mapped,  mapped_column

from sqlalchemy.orm import declarative_base

BaseUser = declarative_base()


class User(SQLAlchemyBaseUserTable[int], BaseUser):
    #we just correct id type
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    


