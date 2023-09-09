<!-- ref for FastAPI : https://fastapi.tiangolo.com/tutorial/first-steps/ -->
<!-- ref for HTTP method  : https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods -->
<!-- SQL (Relational)Databases: https://fastapi.tiangolo.com/tutorial/sql-databases/  -->

<!-- 

We can use below url to test our APIS this will provided by FastAPI itself

http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
 
 -->

<!-- Install virtual env -->
>>> virtualenv venv
<!-- Activate venv -->
<!-- Install fastapi[all]
This 'all' will install all the relevant libraries
 -->
>>> pip install fastapi[all]    
>>> pip freeze   
>>> pip freeze > requirements.txt
<!-- In below line main is our file name and app is our instant name from the file
This will start our server -->
>>> uvicorn main:app


<!-- below are the crude opration methods
Create  : POST
Read    : GET
Update  : PUT/PATCH
Delete  : DELETE
 -->

 <!-- created new folder with name app and create python file '__init__.py' -->
 <!-- Moved main file under the app directory  -->
 <!-- now we run the below command to activate the server -->

>>> uvicorn app.main:app --reload




<!-- ------------  Postgres Database  ------------ -->

<!-- 1. Check if Postgres is Active -->
>>>sudo systemctl is-active postgresql
<!-- 2. Check if Postgres is enabled -->
>>>sudo systemctl is-enabled postgresql
<!-- 3. Check Postgres Service status -->
>>>sudo systemctl status postgresql
<!-- 4. Check if Postgres is ready to accept connections -->
>>>sudo pg_isready
<!-- To start  -->
>>>sudo su - postgres

<!-- Psycopg to perform postgresql database in python-->
>>>pip install psycopg2


>>>pip install sqlalchemy


<!-- ORM -->

<!-- create file database.py and models.py -->
<!-- After that bind model in main file -->
<!-- Create seperate schemas file to hold all schemas -->

<!--Need to install passlib and bcrypt library to convert our password from plaint text to hash -->
<!-- we can not reverse engineer the hash password -->
>>>pip install passlib[bcrypt]

<!-- 

Create one floder
setup virtual env
requirements.txt file

-->
<!-- 

create app folder and under that create __init__.py file
create main.py, models.py, database.py, schemas.py , utils.py under app folder 
main.py file wrape all the files together
models.py hold the ORM
database.py hold the database connectivity
schemas.py hold the all the shemas for functions
utils.py hold passwords related thing

-->

<!-- 

Created new folder "routers" under app to avoid confusion
Add files for specific use
in the main.py file we'll wrape these files using below syntax
 
app.include_router(post.router)
app.include_router(user.router)

-->

<!-- need to install library for singin and verifying JWT token -->
>>> pip install python-jose[cryptography]

<!-- to handle authentication and JWT token we will create new file 'oath2.py'  under app -->

<!-- To get the randome hex string we can use below command -->
openssl rand -hex 32


<!-- create confg file to hold configeration -->
<!-- create .env file and add credentials under that -->



<!-- ------------  Postgres Database  ------------ -->

<!-- Create git repo from git -->
<!-- add git in project using  -->
>>> git init
>>> git add --all
<!-- create branch -->
>>> git branch -M main
<!-- add origin -->
>>> git remote add origin https://github.com/sunnypy22/FastAPI.git
>>> git push -u origin main

<!-- Install alembic which is used as data migration tool -->

>>> pip install alembic

<!-- initiate alembic file by using belopw command , this will create alembic dir in current project -->
<!-- last alembic is folder name -->
>>>alembic init alembic 