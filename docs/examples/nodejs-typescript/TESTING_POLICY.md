# Testing Policy (Node.js + TypeScript)

Keep test runs aligned with change scope and release expectations.

## Testing Approach

This project uses:

- **Jest**: For fast, isolated unit tests of pure logic (services, utils, domain logic)
- **Supertest**: For integration tests of API endpoints and middleware
- **Playwright** (optional): For end-to-end browser testing

## Required Before PR

Run the test suite to ensure all tests pass:

```bash
npm test
```

At minimum, run the fast unit tests:

```bash
npm run test:unit
```

If no automated tests exist yet, provide a short, repeatable manual checklist (steps + expected outcome) in the PR.

### Current Test Suites

**Unit Tests** (fast, isolated):
- `src/**/__tests__/*.test.ts` - Jest unit tests for services, utils, domain logic

**Integration Tests** (API/database):
- `tests/integration/*.test.ts` - Supertest integration tests for API endpoints

**E2E Tests** (optional, browser workflows):
- `tests/e2e/*.spec.ts` - Playwright end-to-end tests

### Running Individual Tests

**Unit Tests:**
```bash
# Run all unit tests
npm run test:unit

# Run specific unit test file
npm test -- src/services/__tests__/auth.service.test.ts

# Run tests in watch mode (for development)
npm run test:watch
```

**Integration Tests:**
```bash
# Run all integration tests
npm run test:integration

# Run specific integration test
npm test -- tests/integration/auth.test.ts
```

**E2E Tests:**
```bash
# Run all e2e tests
npm run test:e2e

# Run specific e2e test
npx playwright test tests/e2e/login.spec.ts
```

## Run When Relevant

- Authentication changes: `auth.service.test.ts`, `tests/integration/auth.test.ts`
- Database schema changes: All integration tests
- API endpoint changes: Relevant integration tests
- Frontend changes: E2E tests

## Release/Pre-merge Sweep

- Run all available automated suites: `npm test`
- Test the core user workflow in the UI
- Include test output/coverage in the PR description

## Writing New Tests

### When to Write Unit Tests

Write Jest unit tests for:
- Service layer logic (AuthService, UserService, etc.)
- Utility functions (data transformations, validators)
- Domain logic and business rules
- Pure functions without external dependencies

**Example structure:**
```typescript
import { AuthService } from '../auth.service';

describe('AuthService', () => {
  let authService: AuthService;

  beforeEach(() => {
    authService = new AuthService();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should hash password correctly', async () => {
    const password = 'test123';
    const hashed = await authService.hashPassword(password);

    expect(hashed).not.toBe(password);
    expect(hashed.length).toBeGreaterThan(20);
  });

  it('should validate correct password', async () => {
    const password = 'test123';
    const hashed = await authService.hashPassword(password);
    const isValid = await authService.validatePassword(password, hashed);

    expect(isValid).toBe(true);
  });
});
```

Place unit tests in: `src/**/__tests__/` (co-located with source files)

### When to Write Integration Tests

Write Supertest integration tests for:
- API endpoint behavior
- Request/response validation
- Authentication/authorization flows
- Database operations
- Middleware chains

**Example structure:**
```typescript
import request from 'supertest';
import { app } from '../src/app';
import { db } from '../src/db';

describe('POST /api/auth/login', () => {
  beforeAll(async () => {
    await db.connect();
  });

  afterAll(async () => {
    await db.disconnect();
  });

  beforeEach(async () => {
    await db.clear();
  });

  it('should return 200 and token for valid credentials', async () => {
    // Arrange
    await db.users.create({ email: 'test@example.com', password: 'hashed...' });

    // Act
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'test@example.com', password: 'test123' });

    // Assert
    expect(response.status).toBe(200);
    expect(response.body.token).toBeDefined();
  });

  it('should return 401 for invalid credentials', async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ email: 'wrong@example.com', password: 'wrong' });

    expect(response.status).toBe(401);
  });
});
```

Place integration tests in: `tests/integration/`

### Test Guidelines

- Don't alter existing tests without explicit approval and rationale
- Add new targeted tests alongside new features/fixes; keep them deterministic
- Prefer unit tests for fast feedback; use integration tests for API/database validation
- All tests should run in CI (GitHub Actions, etc.)
- Use descriptive test names: `it('should [expected behavior] when [condition]')`
- Keep tests focused: one assertion concept per test
- Mock external dependencies in unit tests; use real dependencies in integration tests

## Test Coverage Goals

- **Critical paths (auth, payments):** 90%+ coverage
- **Service layer:** 80%+ coverage
- **Overall project:** 70%+ coverage

Check coverage with:
```bash
npm run test:coverage
```
