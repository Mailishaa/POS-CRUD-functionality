# Boutique POS API

A RESTful Point of Sale (POS) backend API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

The API provides functionality for managing users, customers, products, categories, suppliers, sales, sale items, payments, and receipts. It also includes authentication and role-based authorization.

## Features

* User registration and authentication
* JWT-based authentication
* Role-based authorization
* Customer management
* Product management
* Category management
* Supplier management
* Sales management
* Sale item management
* Payment management
* Receipt management
* PostgreSQL database support
* SQLAlchemy ORM
* API validation with Pydantic
* Automated API tests with pytest
* Interactive API documentation with Swagger UI

## Technology Stack

* **Python 3.12**
* **FastAPI**
* **Uvicorn**
* **SQLAlchemy**
* **PostgreSQL**
* **Alembic**
* **Pydantic**
* **JWT / PyJWT**
* **bcrypt**
* **pytest**
* **pytest-cov**

## Project Structure

```text
pos/
├── app/
│   ├── core/
│   │   └── security.py
│   ├── models/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── database.py
│   ├── dependencies.py
│   └── main.py
├── tests/
├── .env
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── requirements.txt
└── README.md
```

The application follows a layered structure:

```text
API Routers
     ↓
Services
     ↓
Repositories
     ↓
SQLAlchemy Models
     ↓
PostgreSQL
```

This separates API handling, business logic, database operations, and data models.

## Requirements

Make sure you have:

* Python 3.12+
* PostgreSQL
* pip or uv
* Git

## Installation

Clone the repository:

```bash
git clone https://github.com/Mailishaa/POS-CRUD-functionality.git
cd POS-CRUD-functionality
```

Create and activate a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

If you use `uv`:

```bash
uv pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql://username:password@localhost:5432/pos
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace the database credentials with your local PostgreSQL configuration.

**Do not commit `.env` to Git.**

## Database

Create a PostgreSQL database for the application.

Example:

```sql
CREATE DATABASE pos;
```

Update the `DATABASE_URL` in `.env` to point to the database.

Alembic configuration is included for database migration management.

## Running the API

Activate the virtual environment:

```bash
source env/bin/activate
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://127.0.0.1:8000
```

## API Documentation

FastAPI automatically provides interactive documentation.

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

## Authentication

Protected endpoints require a JWT access token.

First authenticate through the login endpoint. The returned access token can then be supplied using the HTTP `Authorization` header:

```text
Authorization: Bearer <access_token>
```

The API also uses role-based authorization for operations that require administrator privileges.

## Main API Resources

The API provides endpoints for:

| Resource      | Purpose              |
| ------------- | -------------------- |
| `/auth`       | Authentication       |
| `/users`      | User management      |
| `/customers`  | Customer management  |
| `/products`   | Product management   |
| `/categories` | Category management  |
| `/suppliers`  | Supplier management  |
| `/sales`      | Sales management     |
| `/sale-items` | Sale item management |
| `/payments`   | Payment management   |
| `/receipts`   | Receipt management   |

The exact available endpoints and request/response schemas can be viewed through the Swagger documentation at `/docs`.

## Running Tests

Run the complete test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=. --cov-report=term-missing
```

The project is configured to require at least **90% test coverage**.

## API Health Check

The application includes a root endpoint that can be used to confirm that the API is running:

```bash
curl http://127.0.0.1:8000/
```

A successful response is:

```json
{
  "message": "Boutique POS API is running successfully"
}
```

## Development

When making changes:

1. Create or switch to a feature branch.
2. Make the required changes.
3. Run the test suite.
4. Check test coverage.
5. Commit the changes with a clear commit message.
6. Push the branch to GitHub.

Example:

```bash
git checkout -b feature/my-change
```

Run tests:

```bash
pytest
```

Commit:

```bash
git add .
git commit -m "feat: describe the change"
```

Push:

```bash
git push origin feature/my-change
```


