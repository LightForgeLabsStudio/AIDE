# Coding Guidelines (Node.js + TypeScript)

Standards for TypeScript/Node.js projects using AIDE.

## Core Principles

- **Type safety:** Leverage TypeScript's type system; avoid `any`
- **Async/await:** Use async/await over raw Promises; handle errors properly
- **Immutability:** Prefer const, avoid mutations when possible
- **Single responsibility:** Functions/classes should do one thing well
- **Small, focused changes:** Prefer minimal diffs with tests and docs

## TypeScript Style

Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript) with TypeScript extensions.

### Naming Conventions

- **camelCase**: variables, functions, methods (`getUserById`, `currentUser`)
- **PascalCase**: classes, interfaces, types (`UserService`, `ApiResponse`)
- **UPPER_SNAKE_CASE**: constants (`MAX_RETRY_COUNT`, `API_BASE_URL`)
- **kebab-case**: file names (`user.service.ts`, `auth.middleware.ts`)

### Code Organization

- Use clear, descriptive names; avoid abbreviations
- Add JSDoc comments for public APIs
- Keep functions small (< 50 lines ideally)
- Use TypeScript enums for fixed sets of values
- Prefer interfaces over types for object shapes

Example:
```typescript
/**
 * Authenticates a user with email and password.
 * @param email - User's email address
 * @param password - Plain text password
 * @returns Authentication token
 * @throws {UnauthorizedError} If credentials are invalid
 */
async function authenticateUser(email: string, password: string): Promise<string> {
  // Implementation
}
```

## Architecture Boundaries

- **Controllers**: Handle HTTP request/response; delegate to services
- **Services**: Contain business logic; no HTTP knowledge
- **Repositories**: Handle data access; abstract database details
- **Middleware**: Cross-cutting concerns (auth, logging, validation)
- **Utils**: Pure functions with no side effects

## Error Handling

```typescript
// Custom error classes
class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NotFoundError';
  }
}

// Async error handling
try {
  const user = await userService.getById(id);
  return user;
} catch (error) {
  if (error instanceof NotFoundError) {
    throw new HttpException(404, error.message);
  }
  throw error;
}
```

## Testing

See [TESTING_POLICY.md](TESTING_POLICY.md).

- Mock external dependencies in unit tests
- Use real database (with test data) in integration tests
- Test error cases, not just happy paths

## Git Commits

- Use conventional commits: `feat:`, `fix:`, `refactor:`, `test:`, `docs:`
- Keep commits atomic and single-purpose
- Run `npm run lint` and `npm test` before committing

## Reference Docs

- [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
