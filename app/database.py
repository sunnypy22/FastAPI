from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_IRL is the variable name
# SQLALCHEMY_DATABASE_IRL = 'postgresql://<username>:<password>@<ip-address/hostname>/<databasename>'

SQLALCHEMY_DATABASE_IRL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_IRL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# For Reference
while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'fadtapi',user='postgres',
                                password='root', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("data base connection was successfully done")
        break

    except Exception as error:
        print("Connecting to data base failed")
        print("Error :", error)
        time.sleep(3)
