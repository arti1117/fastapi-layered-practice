# pip install python-dotenv
import os
import sys
from pathlib import Path

# Add project root to Python path to enable imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
from fastapi import FastAPI

from config.mysql_config import Base, engine

load_dotenv()

app = FastAPI()

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("APP_HOST")
    port = int(os.getenv("APP_PORT"))
    Base.metadata.create_all(bind=engine)
    uvicorn.run(app, host=host, port=port)
