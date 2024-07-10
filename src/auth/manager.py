""""Just standard methods for User Manager implementation and creation: 
https://fastapi-users.github.io/fastapi-users/latest/configuration/user-manager/ """

from typing import Optional, Annotated, AsyncGenerator, Any
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, IntegerIDMixin
from auth.models import User
from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_async_session


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        print(f"User {user.id} has registered.")


async def get_user_db(session: Annotated[AsyncGenerator[AsyncSession, None], Depends(get_async_session)]):
    yield SQLAlchemyUserDatabase(session, User)

async def get_user_manager(user_db: Annotated[AsyncGenerator[SQLAlchemyUserDatabase[User, Any], Any], Depends(get_user_db)]):
    yield UserManager(user_db)

    

