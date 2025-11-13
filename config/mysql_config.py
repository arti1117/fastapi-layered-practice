import os
import urllib
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables before using them
load_dotenv()

password = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD"))
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv("MYSQL_USER")}:{password}"
    f"@{os.getenv('MYSQL_HOST')}:{os.getenv('MYSQL_PORT')}/{os.getenv('MYSQL_DATABASE')}"
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
