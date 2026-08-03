from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from dotenv import load_dotenv
import os
load_dotenv() 


db_url = os.getenv("SQLALCHEMY_DATABASE_URL") 

engine = create_engine(db_url)




SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session  routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
