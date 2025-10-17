# CJW Backend

This is the backend service for the CJW application built with FastAPI and MySQL.

## Requirements

- Docker
- Docker Compose

## Project Structure

```
backend/
├── app/
│   ├── config/
│   │   └── database.py
│   ├── managers/
│   │   ├── db_manager.py
│   │   ├── file_manager.py
│   │   └── scrapper_manager.py
│   ├── sources/
│   │   └── templates/
│   │       └── home.html
│   ├── db.json
│   ├── jwt_manager.py
│   ├── main.py
│   ├── schemes.py
│   ├── view_members.py
│   └── view_users.py
├── Dockerfile
└── requirements.txt
```

## Development

### Running with Docker Compose

To run the backend service along with the frontend and database:

```bash
docker compose up
```

This will start:
- The backend service on port 8080
- The MySQL database on port 33061

### Running Locally

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI application:
```bash
uvicorn app.main:app --reload --port 8080
```

## API Documentation

Once the server is running, you can access:
- Swagger UI documentation at: http://localhost:8080/docs
- ReDoc documentation at: http://localhost:8080/redoc

## Database

The application uses MySQL as its database. Connection details:
- Host: localhost (or db in Docker)
- Port: 33061
- Database: cjw_db
- Username: root
- Password: root