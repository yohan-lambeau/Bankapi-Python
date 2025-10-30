# Banking API - Python

A secure REST API for banking operations built with FastAPI, featuring JWT authentication, password hashing, and comprehensive banking functionality.

## Features

- **Authentication & Security**
  - JWT token-based authentication
  - Password hashing with bcrypt
  - Protected endpoints requiring authentication
  - Bearer token authorization

- **User Management**
  - User registration with email validation
  - Secure login with token generation
  - User profile management

- **Account Management**
  - Create bank accounts (checking, savings, etc.)
  - View all user accounts
  - View individual account details
  - Delete accounts
  - Unique account number generation

- **Transaction Management**
  - Deposit money
  - Withdraw money (with balance validation)
  - View transaction history
  - Transaction types: deposit, withdrawal, transfer

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - SQL toolkit and ORM
- **Pydantic** - Data validation using Python type annotations
- **python-jose** - JWT token handling
- **passlib** - Password hashing with bcrypt
- **uvicorn** - ASGI server

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yohan-lambeau/Bankapi-Python.git
cd Bankapi-Python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token

### Accounts (Protected)
- `POST /accounts/` - Create a new account
- `GET /accounts/` - Get all user accounts
- `GET /accounts/{account_id}` - Get specific account
- `DELETE /accounts/{account_id}` - Delete an account

### Transactions (Protected)
- `POST /transactions/{account_id}` - Create a transaction
- `GET /transactions/{account_id}` - Get account transaction history

## Usage Examples

### Register a User
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "secretpass123",
    "full_name": "John Doe"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "secretpass123"
  }'
```

### Create Account (with authentication)
```bash
curl -X POST "http://localhost:8000/accounts/" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "account_type": "checking",
    "currency": "USD"
  }'
```

### Create Transaction
```bash
curl -X POST "http://localhost:8000/transactions/1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "transaction_type": "deposit",
    "amount": 100.50,
    "description": "Initial deposit"
  }'
```

## Testing

Run tests using pytest:
```bash
pip install pytest httpx
pytest tests/
```

## Security Features

1. **Password Security**: Passwords are hashed using bcrypt before storage
2. **JWT Tokens**: Secure token-based authentication with configurable expiration
3. **Authorization**: Protected endpoints require valid bearer tokens
4. **Input Validation**: All inputs validated using Pydantic models
5. **SQL Injection Protection**: SQLAlchemy ORM prevents SQL injection attacks

## Configuration

Create a `.env` file in the root directory to customize settings:
```
SECRET_KEY=your-secret-key-change-in-production-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./bank.db
```

### Production Deployment Notes

⚠️ **IMPORTANT**: Before deploying to production:

1. **Generate a secure secret key**:
   ```bash
   openssl rand -hex 32
   ```
   Set this value in your `.env` file or environment variables.

2. **Configure CORS**: Update `app/main.py` to specify allowed origins instead of `["*"]`

3. **Use a production database**: Replace SQLite with PostgreSQL or MySQL for production

4. **Enable HTTPS**: Use a reverse proxy (nginx) with SSL certificates

5. **Environment Variables**: Never commit secrets to version control. Use environment variables or secret management services.

## Project Structure

```
Bankapi-Python/
├── app/
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── security.py        # Security utilities
│   ├── models/
│   │   ├── database.py        # Database setup
│   │   └── models.py          # SQLAlchemy models
│   ├── routers/
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── accounts.py        # Account endpoints
│   │   └── transactions.py    # Transaction endpoints
│   ├── schemas/
│   │   └── schemas.py         # Pydantic schemas
│   └── main.py                # FastAPI application
├── tests/
│   └── test_api.py            # API tests
├── requirements.txt           # Dependencies
└── README.md                  # Documentation
```

## License

This project is open source and available under the MIT License.