# Testing Policy (Python)

Testing standards for Python projects using AIDE.

## Testing Approach

This project uses:

- **pytest**: For unit and integration tests
- **pytest-cov**: For coverage reporting
- **pytest-mock**: For mocking dependencies

## Required Before PR

Run the test suite:

```bash
pytest
```

Run fast unit tests only:

```bash
pytest tests/unit
```

## Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=src --cov-report=html

# Specific test file
pytest tests/unit/test_auth.py

# Specific test function
pytest tests/unit/test_auth.py::test_hash_password

# Watch mode (requires pytest-watch)
ptw
```

## Writing Tests

### Unit Test Example

```python
import pytest
from src.services.auth import AuthService

@pytest.fixture
def auth_service():
    return AuthService()

def test_hash_password(auth_service):
    password = "test123"
    hashed = auth_service.hash_password(password)

    assert hashed != password
    assert len(hashed) > 20

def test_validate_password(auth_service):
    password = "test123"
    hashed = auth_service.hash_password(password)

    assert auth_service.validate_password(password, hashed) is True
    assert auth_service.validate_password("wrong", hashed) is False
```

### Integration Test Example

```python
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    # Setup
    db = get_db()
    db.clear()
    yield
    # Teardown
    db.clear()

def test_login_success():
    # Arrange
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "test123"
    })

    # Act
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "test123"
    })

    # Assert
    assert response.status_code == 200
    assert "token" in response.json()
```

## Coverage Goals

- Core business logic: 90%+
- Overall project: 80%+

Run coverage: `pytest --cov=src --cov-report=term-missing`
