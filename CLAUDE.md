# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

**Start the application:**
```bash
# Activate virtual environment first
source .venv/bin/activate

# Run using the runner script (handles path setup and DB initialization)
python run.py
```

**Access the application:**
- API: http://localhost:33333
- Swagger UI: http://localhost:33333/docs
- ReDoc: http://localhost:33333/redoc

## Development Commands

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**MySQL Database (Docker):**
```bash
# Start MySQL container
docker run -d \
  --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=fastapi_test_db \
  -e MYSQL_USER=arti \
  -e MYSQL_PASSWORD=arti@1234 \
  -p 3306:3306 \
  mysql:8

# Check MySQL is running
docker ps | grep mysql

# Test connection
docker exec mysql-container mysql -u arti -p'arti@1234' -e "SHOW DATABASES;"
```

## Architecture

This is a **layered architecture** FastAPI project following clean separation of concerns.

### Core Design Principles

**Layered Module Structure:**
Each domain module (e.g., `anonymous_board/`) follows this 4-layer pattern:
- `entity/` → SQLAlchemy models (database schema)
- `repository/` → Data access layer (database operations)
- `service/` → Business logic layer
- `controller/` → API endpoints (FastAPI routes)

**Dependency Flow:**
```
controller → service → repository → entity
```
Controllers call services, services call repositories, repositories use entities. Never skip layers.

### Project Structure

```
project_root/
├── app/
│   └── main.py              # FastAPI app instance
├── config/
│   └── mysql_config.py      # SQLAlchemy engine, Base, SessionLocal
├── [domain_module]/         # e.g., anonymous_board/
│   ├── entity/              # SQLAlchemy models
│   ├── repository/          # Database operations
│   ├── service/             # Business logic
│   └── controller/          # FastAPI routes
├── run.py                   # Application entry point
├── requirements.txt
└── .env                     # Database credentials (not in git)
```

### Python Path Setup

**Critical:** This project uses `sys.path.insert(0, project_root)` for imports.

- `run.py` handles path setup automatically
- All imports use absolute paths from project root: `from config.mysql_config import Base`
- Never use relative imports like `from ..config import Base`

### Database Configuration

**Database initialization happens in run.py:**
```python
Base.metadata.create_all(bind=engine)  # Creates tables on startup
```

**Connection string format:**
```python
# Password is URL-encoded (see mysql_config.py)
mysql+pymysql://{user}:{encoded_password}@{host}:{port}/{database}
```

**Environment variables (from .env):**
- `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_DATABASE`, `MYSQL_PORT`
- `APP_HOST`, `APP_PORT`

### Adding New Features

When adding a new domain module (e.g., `user/`, `post/`):

1. **Create the 4-layer structure:**
   ```
   new_module/
   ├── __init__.py
   ├── entity/
   │   ├── __init__.py
   │   └── new_model.py      # SQLAlchemy model inheriting from Base
   ├── repository/
   │   ├── __init__.py
   │   └── new_repository.py # DB operations using SessionLocal
   ├── service/
   │   ├── __init__.py
   │   └── new_service.py    # Business logic calling repository
   └── controller/
       ├── __init__.py
       └── new_controller.py # FastAPI routes calling service
   ```

2. **Entity pattern (SQLAlchemy model):**
   ```python
   from sqlalchemy import Column, String, DateTime
   from config.mysql_config import Base

   class YourModel(Base):
       __tablename__ = 'your_table'
       id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
       # ... other columns
   ```

3. **Repository pattern (database operations):**
   ```python
   from config.mysql_config import SessionLocal

   def create_item(data):
       db = SessionLocal()
       try:
           # DB operations
           db.commit()
       finally:
           db.close()
   ```

4. **Service pattern (business logic):**
   ```python
   from .repository import new_repository

   def handle_business_logic(data):
       # Validate, transform, call repository
       return new_repository.create_item(data)
   ```

5. **Controller pattern (FastAPI routes):**
   ```python
   from fastapi import APIRouter
   from .service import new_service

   router = APIRouter(prefix="/api/endpoint")

   @router.post("/")
   def create_endpoint(request: YourSchema):
       return new_service.handle_business_logic(request)
   ```

6. **Register router in app/main.py:**
   ```python
   from new_module.controller.new_controller import router as new_router
   app.include_router(new_router)
   ```

### Current Implementation Status

**Implemented:**
- `anonymous_board` module structure (entity layer complete with AnonymousBoard model)
- Database configuration with SQLAlchemy
- FastAPI application setup with automatic table creation

**Incomplete:**
- `anonymous_board` repository, service, and controller layers are empty
- No API endpoints registered yet

### Database Session Management

Sessions are created per-operation in repositories:
```python
db = SessionLocal()
try:
    # operations
    db.commit()
finally:
    db.close()
```

Alternative: Use FastAPI dependency injection for automatic session management.
