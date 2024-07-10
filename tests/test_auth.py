import pytest
from httpx import AsyncClient

from conftest import GetJson, register, login



@pytest.mark.parametrize("testcase", GetJson())
class TestAuth():

    """We take test cases data from the file into testcase list and use this list in the tests"""

    def _GetStatus(self, testcase, par):
        try:
            #login and register have different successful responses
            if type(testcase["status_code"]) is dict:
                checking_status = testcase["status_code"][par]
            else:
                checking_status = testcase["status_code"]
            return checking_status
        except:
            print("QA error")
    

    async def test_register(self, ac: AsyncClient, testcase):
        response = await register(ac, email=testcase["user"], password=testcase["password"])
        assert response.status_code == self._GetStatus(testcase, "register")


    async def test_double_register(self, ac: AsyncClient, testcase):
        """the case when a user tries to register again"""
        response = await register(ac, email=testcase["user"], password=testcase["password"])
        checking_status = self._GetStatus(testcase, "login")
        if (checking_status == 201) and (response.status_code == checking_status):
            response = await register(ac, email=testcase["user"], password=testcase["password"])
            assert response.status_code == 400


    async def test_login(self, ac: AsyncClient, testcase):
        await register(ac, email=testcase["user"], password=testcase["password"])
        response = await login(ac, email=testcase["user"], password=testcase["password"])
        checking_status = self._GetStatus(testcase, "login")
        assert response.status_code == checking_status

        if checking_status == 200:
            assert len(response.json()["access_token"]) > 5 


    async def test_nonexist_login(self, ac: AsyncClient, testcase):
        """the case when a user did not register before login"""
        response = await login(ac, email=testcase["user"], password=testcase["password"])
        checking_status = self._GetStatus(testcase, "login")
        if checking_status != 422:  #if we check the test case with non empty login and password
            assert response.status_code == 400  
        else:
            assert response.status_code == self._GetStatus(testcase, "login") 

    
