# FastAPI Layered Practice

A FastAPI project with layered architecture for practicing clean code organization and database integration.

## Project Structure

```
fastapi-layered-practice/
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI application entry point
├── config/
│   ├── __init__.py
│   └── mysql_config.py   # Database configuration
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── run.py               # Application runner with proper path setup
└── README.md
```

## Prerequisites

- Python 3.8+
- MySQL 8.0 (running in Docker or locally)
- Virtual environment

## Setup Instructions

### 1. Install Dependencies

```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 2. Configure Environment

Create or verify `.env` file with your database credentials:

```env
APP_HOST=0.0.0.0
APP_PORT=33333

MYSQL_HOST=localhost
MYSQL_USER=arti
MYSQL_PASSWORD=arti@1234
MYSQL_DATABASE=fastapi_test_db
MYSQL_PORT=3306
```

### 3. Start MySQL Database

If using Docker:

```bash
docker run -d \
  --name mysql-container \
  -e MYSQL_ROOT_PASSWORD=root \
  -e MYSQL_DATABASE=fastapi_test_db \
  -e MYSQL_USER=arti \
  -e MYSQL_PASSWORD=arti@1234 \
  -p 3306:3306 \
  mysql:8
```

### 4. Run the Application

```bash
# Activate virtual environment
source .venv/bin/activate

# Run using the provided runner script
python run.py
```

The application will be available at: `http://0.0.0.0:33333`

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'pymysql'
**Solution**: Install pymysql - `pip install pymysql`

### Issue: ModuleNotFoundError: No module named 'config'
**Solution**: Use the provided `run.py` script which sets up the Python path correctly

### Issue: Can't connect to MySQL server
**Solution**:
- Verify MySQL is running: `docker ps | grep mysql`
- Check MySQL credentials in `.env` match your database
- Test connection: `docker exec mysql-container mysql -u arti -p'arti@1234' -e "SHOW DATABASES;"`

### Issue: Port already in use
**Solution**: Change `APP_PORT` in `.env` to an available port

## Development

The application uses:
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: ORM for database operations
- **PyMySQL**: MySQL database driver
- **Uvicorn**: ASGI server for running the application
- **python-dotenv**: Environment variable management

## Database Tables

Database tables will be automatically created on application startup based on SQLAlchemy models.

## API Documentation

Once running, access interactive API documentation at:
- Swagger UI: `http://localhost:33333/docs`
- ReDoc: `http://localhost:33333/redoc`

## Verified Working

✅ All dependencies installed
✅ MySQL database connection established
✅ Application starts successfully
✅ Database tables created automatically
✅ Environment configuration working
