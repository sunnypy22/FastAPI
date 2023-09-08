from fastapi import FastAPI, HTTPException, Response, status
from fastapi.params import Body, Depends
# here pydantic is the library which is already in env because we have used fastapi[all]
from typing import Optional, List
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db
from . import models, schemas
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# Binding the models
models.Base.metadata.create_all(bind=engine)

# here app is the instant , we can give any name
app = FastAPI()

origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


"""
1] here is the decorator which holds the endpoint and menthod
2] whenever we make the changes under def then we have to restart the server
3] If we don't wanna restart the server after changes then we can use 
'uvicorn main:app --reload' instead  'uvicorn main:app'
"""

@app.get("/")
def root():
    return {"message": "Hello There"}



"""
1] Here is the post request
2] We can get the data whatever we  gave under the body for that we need to pass parameter 
   under POST method
3] payload is the variable name , we can give any of the name
"""
@app.post("/createposts")
def create_posts(payload : dict = Body(...)):
    print(payload)
    return{
        "message" : f"Our message is {payload['message']} and method is {payload['method']}"
    }
    # return {"message": "Successfully created posts"}


# we can perform crude for the data which we'll store in memory


"""
we can change the default status by passing params in def
"""

memory_loc = []

# @app.post("/crd_get_posts",status_code=status.HTTP_201_CREATED)
@app.post("/crd_get_posts",status_code=status.HTTP_201_CREATED)

def crd_get_posts(new_posts:schemas.Post, response:Response):
    # we can convert the variable in dict as well
    new_posts.dict()
    memory_loc.append(new_posts)
    if not memory_loc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message' : "Not found"}
    return {"message" : memory_loc}


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

