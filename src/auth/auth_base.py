"""The file is used for combining the transport and strategy, and for the token validation"""

from fastapi_users.authentication import BearerTransport, AuthenticationBackend, CookieTransport
from fastapi_users.authentication import JWTStrategy
from config import settings
from fastapi_users import FastAPIUsers
from auth.manager import get_user_manager, get_user_db
from auth.models import User
from logging import error
from fastapi import HTTPException
from inspect import currentframe


#cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name="Posts")
bearer_transport = BearerTransport(tokenUrl="auth/login")

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.SECRETa, lifetime_seconds=settings.JWT_LIFETIME_MINUTES*60)


#We create an Authentication Backend that will consist of a JWT strategy and a Bearer transport method 
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
    )

#Configure FastAPIUsers object with the elements we defined before
fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


async def verify_token(token: str, session):
    """The function is used for token validation. 
    It was added because we will receive a token in the Post endpoints, not a useremail and password"""
    current_func = currentframe().f_code.co_name
    if not token:
        raise HTTPException(status_code=401, detail='Not valid token')
    
    try:
    #we use the function read_token from the fastapi-users library
        curent_strategy = get_jwt_strategy()
        async for userdb in get_user_db(session):
            async for user_manager in get_user_manager(userdb):
                read_user = await curent_strategy.read_token(token, user_manager)
                useremail = read_user.email
    except Exception as e:
        error(f"{current_func} Unauthorized error: {e}")
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        return useremail
    
    
