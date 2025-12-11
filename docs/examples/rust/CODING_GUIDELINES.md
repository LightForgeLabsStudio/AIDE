# Coding Guidelines (Rust)

Standards for Rust projects using AIDE.

## Core Principles

- **Follow Rust idioms**: Use The Rust Book patterns
- **Ownership and borrowing**: Leverage Rust's memory safety
- **Error handling**: Use Result/Option, avoid panics in library code
- **Type safety**: Use strong types, avoid primitives

## Rust Style

Follow [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/).

### Naming Conventions

- **snake_case**: functions, variables, modules (`get_user_by_id`, `current_user`)
- **PascalCase**: types, traits (`UserService`, `Serialize`)
- **SCREAMING_SNAKE_CASE**: constants (`MAX_RETRY_COUNT`)

### Code Organization

```rust
//! Module documentation.

use std::error::Error;

/// Service for managing users.
pub struct UserService {
    db: DatabasePool,
}

impl UserService {
    /// Creates a new UserService.
    pub fn new(db: DatabasePool) -> Self {
        Self { db }
    }

    /// Retrieves a user by ID.
    ///
    /// # Errors
    ///
    /// Returns `UserNotFound` if user doesn't exist.
    pub async fn get_by_id(&self, id: i64) -> Result<User, ServiceError> {
        // Implementation
    }
}
```

## Error Handling

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum ServiceError {
    #[error("User not found: {0}")]
    UserNotFound(i64),

    #[error("Database error")]
    DatabaseError(#[from] sqlx::Error),
}

// Usage
fn get_user(id: i64) -> Result<User, ServiceError> {
    db.query_as("SELECT * FROM users WHERE id = $1")
        .bind(id)
        .fetch_one()
        .await?
        .ok_or(ServiceError::UserNotFound(id))
}
```

## Formatting

```bash
cargo fmt
cargo clippy
```

## Reference Docs

- [The Rust Book](https://doc.rust-lang.org/book/)
- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
