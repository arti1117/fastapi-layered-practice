#!/usr/bin/env python3
"""
FastAPI Application Runner
Ensures proper Python path configuration for module imports
"""
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Now import and run the application
if __name__ == "__main__":
    from app.main import app
    from config.mysql_config import Base, engine
    import os
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()

    # Create database tables
    Base.metadata.create_all(bind=engine)

    # Run the application
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("APP_PORT", "8000"))

    print(f"🚀 Starting FastAPI application on http://{host}:{port}")
    uvicorn.run(app, host=host, port=port)
