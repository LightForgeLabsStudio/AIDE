# Testing Policy (Rust)

Testing standards for Rust projects using AIDE.

## Testing Approach

- **cargo test**: Built-in testing framework
- **Unit tests**: Co-located with source code
- **Integration tests**: In `tests/` directory

## Required Before PR

```bash
cargo test
```

## Running Tests

```bash
# All tests
cargo test

# Unit tests only
cargo test --lib

# Integration tests only
cargo test --test '*'

# Specific test
cargo test test_auth

# With output
cargo test -- --nocapture

# With coverage (requires tarpaulin)
cargo tarpaulin --out Html
```

## Writing Tests

### Unit Test Example

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_hash_password() {
        let password = "test123";
        let hashed = hash_password(password);

        assert_ne!(hashed, password);
        assert!(hashed.len() > 20);
    }

    #[test]
    #[should_panic(expected = "Invalid password")]
    fn test_empty_password_panics() {
        hash_password("");
    }
}
```

### Integration Test Example

```rust
// tests/api_tests.rs
use my_app::*;

#[tokio::test]
async fn test_login_success() {
    let app = spawn_app().await;

    let response = app.post_login(&serde_json::json!({
        "email": "test@example.com",
        "password": "test123"
    })).await;

    assert_eq!(response.status(), 200);
    assert!(response.json::<LoginResponse>().await.is_ok());
}
```

## Coverage Goals

- Core logic: 90%+
- Overall: 80%+

Run: `cargo tarpaulin`
