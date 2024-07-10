"""the file for tests configuration. To run tests: $env:ENV_FILE=".test.env"; pytest -v tests/"""

import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import json
from constants import  testing_file


from posts.models import BasePost 
from auth.models import BaseUser
from config import settings
from main import app

#test database and session creation
engine_test = create_async_engine(settings.DB_URL, poolclass=NullPool) 
async_session_maker = sessionmaker(engine_test, class_= AsyncSession, expire_on_commit=False)



@pytest.fixture(autouse=True)
async def prepare_database():
    """the database will be cleared after each test"""
    assert settings.MODE == "TEST"
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseUser.metadata.create_all)
        await conn.run_sync(BasePost.metadata.create_all) 
    yield
    async with engine_test.begin() as conn:  
        await conn.run_sync(BasePost.metadata.drop_all)  
        await conn.run_sync(BaseUser.metadata.drop_all)
        


@pytest.fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()




@pytest.fixture()
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """Pytest fixture to provide an AsyncClient for testing the ASGI app."""
    transport = ASGITransport(app=app)
    
    async with AsyncClient(transport=transport, base_url="http://test") as ac:      
        yield ac



def GetJson() -> list:
    """loading data to use in tests"""
    try:
        f = open(r"tests/auth_testcases.json", 'r')
        UsersDB = json.load(f)
        return UsersDB
    except:
        print('Test JSON can not be loaded')


def readtext() -> str:
    """the function to load big data files"""
    try:
        f = open(testing_file, 'r')
        text = f.read()
        return text
    except:
        print("QA error")
    


async def register(ac: AsyncClient, email, password):
    """to register a test user. Will be used in each test"""
    response = await ac.post('/auth/register', json = {
                "email": email,
                "password": password,
                })

    return response



async def login(ac: AsyncClient, email, password):
    """to login a test user. Will be used in each test"""
    response = await ac.post('/auth/login', data = {
                "username": email,
                "password": password,
                })
    return response

