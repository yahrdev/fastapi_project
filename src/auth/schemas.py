"""Pydantic schemas for working with Users"""

from fastapi_users import schemas
from pydantic import Field
from typing import Optional


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    #we just add a password pattern requirement
    password: str = Field(pattern=r'[a-zA-Z0-9&@%!$~#^*=]', examples=["string&123"])
    
    
    


