# Library Management Backend

Backend Requirements Document for a Library Management Tool built using FastAPI and PostgreSQL.
This backend defines the core architecture, modules, APIs, and security requirements for managing
library operations.It focuses on modular backend design, JWT-based authentication, role-based access
control, standardized REST APIs, and database schema versioning using Alembic. The application is
containerized using Docker and designed to run via Docker Compose.


---

## Tech Stack
- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- Alembic (database migrations)
- JWT Authentication
- Docker & Docker Compose

---

## Features
- Authentication & Authorization (JWT)
- Book Management
- Member Management
- Circulation (Issue, Return, Renew)
- Fine Management
- Search & Reports


---

## Project Structure
library-management-backend/
- ├── app/
- │   ├── main.py
- │   ├── models/
- │   ├── routers/
- │   ├── schemas/
- │   ├── core/
- │   └── utils/
- ├── alembic/
- │   ├── versions/
- │   └── env.py
- ├── alembic.ini
- ├── docker-compose.yml
- ├── Dockerfile
- ├── requirements.txt
- ├── .env.example
- └── README.md

---

## Setup (Docker)

1. Clone the repository

- git clone https://github.com/abhi19833/library-management-backend.git  

2. Create a `.env` file in the project root
- DATABASE_URL=postgresql://username:password@db:5432/dbname  
- JWT_SECRET=your_jwt_secret  

3. Build and start the application
- docker-compose up --build

4. Run database migrations
- docker-compose exec backend alembic upgrade head

5. Access the API
- http://127.0.0.1:8000

---

