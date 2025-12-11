# Coding Guidelines (Python)

Standards for Python projects using AIDE.

## Core Principles

- **Follow PEP 8**: Use Black formatter and flake8 linter
- **Type hints**: Use type annotations for function signatures
- **Explicit is better than implicit**: Clear, readable code over clever code
- **DRY**: Don't repeat yourself
- **Small functions**: Keep functions focused and testable

## Python Style

Follow [PEP 8](https://peps.python.org/pep-0008/) with these specifics:

### Naming Conventions

- **snake_case**: functions, variables, modules (`get_user_by_id`, `current_user`)
- **PascalCase**: classes (`UserService`, `ApiResponse`)
- **UPPER_SNAKE_CASE**: constants (`MAX_RETRY_COUNT`, `API_BASE_URL`)

### Code Organization

```python
"""Module docstring explaining purpose."""

from typing import Optional
import logging

logger = logging.getLogger(__name__)

class UserService:
    """Service for managing users.

    Handles user creation, authentication, and profile management.
    """

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID.

        Args:
            user_id: The user's unique identifier

        Returns:
            User object if found, None otherwise

        Raises:
            DatabaseError: If database connection fails
        """
        # Implementation
        pass
```

## Type Hints

Use type hints for all public functions:

```python
from typing import List, Dict, Optional, Union

def process_users(
    users: List[User],
    filter_active: bool = True
) -> Dict[int, User]:
    """Process and index users."""
    pass
```

## Error Handling

```python
class UserNotFoundError(Exception):
    """Raised when user cannot be found."""
    pass

def get_user(user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
```

## Testing

See [TESTING_POLICY.md](TESTING_POLICY.md).

## Formatting

```bash
# Format code
black src tests

# Check style
flake8 src tests

# Type checking
mypy src
```

## Reference Docs

- [PEP 8](https://peps.python.org/pep-0008/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Black Code Style](https://black.readthedocs.io/)
