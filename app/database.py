from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

from psycopg2.extras import RealDictCursor
import time
from .config import settings
# Create engine for connecting to database
engine = create_engine(
    f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

while True:

    try:
        conn = psycopg2.connect(host='localhost',
                                database='fastapi',
                                user='postgres',
                                password='root',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database connect successfully')
        break
    except Exception as error:
        print("Connecting to database fail !!!")
        print("Error", error)
        time.sleep(2)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base class for declarative models
Base = declarative_base()
