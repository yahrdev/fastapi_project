"""The main file that should be run to execute the app. To run: uvicorn  src.main:app --reload"""
import sys
import os

sys.path.append(os.path.join(sys.path[0], 'src'))

from fastapi import FastAPI, Request, APIRouter

from auth.auth_base import auth_backend, fastapi_users
from auth.schemas import UserCreate, UserRead
from posts.router import router_posts, Validate_Post_Text



tags_metadata = [
    {
        "name": "Auth",
        "description": "The block to manage a user's authorization",
    },
    {
        "name": "Posts",
        "description": "The block to manage the user's posts",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

def select_needed_enpoint(r, path: str):
    #to pick only nessesary endpoint from the standart fastapi-users functionality 

    for route in r.routes:
        if route.path == path:
            NewRouter = APIRouter()
            NewRouter.routes.append(route)     
            return NewRouter      
    return r


routerList = fastapi_users.get_auth_router(auth_backend)
LoginRouter = select_needed_enpoint(routerList, "/login") #logout is not necessary


#the router for Login
app.include_router(
    LoginRouter,
    prefix="/auth",
    tags=["Auth"], 
)                     



#the router for Signup
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
    
)


#Implement request validation to limit the size of the payload for the AddPost endpoint
@app.middleware("http")
async def CheckPostSize(request: Request, call_next):
    return await Validate_Post_Text(request, call_next)
    

#the routers for GetPosts, AddPost and DeletePost
app.include_router(router_posts)  

@app.get("/")
async def read_root(request: Request):
    return {"message": "Open '{}docs' in order to read the endpoints documentation".format(request.base_url)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)