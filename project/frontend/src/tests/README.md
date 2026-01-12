# Frontend Tests

This directory contains unit tests for React components and API clients.

## Structure

```
tests/
├── setup.js                    # Test configuration and setup
├── components/                  # Component tests
│   ├── ResumeList.test.jsx     # ResumeList component tests
│   └── EvaluationPanel.test.jsx # EvaluationPanel component tests
└── api/                         # API client tests
    └── resumes.test.js          # API client tests
```

## Running Tests

### Install Dependencies

```bash
npm install
```

### Run Tests

```bash
npm test
```

### Run Tests with UI

```bash
npm run test:ui
```

### Run Tests with Coverage

```bash
npm run test:coverage
```

### Watch Mode

```bash
npm test -- --watch
```

## Test Configuration

Tests use:
- **Vitest** as the test runner
- **@testing-library/react** for component testing
- **jsdom** for DOM simulation
- **@testing-library/jest-dom** for DOM matchers

## Writing Tests

### Component Tests

Test React components:
- Rendering
- User interactions
- Props handling
- State management

### API Tests

Test API client functions:
- Request/response handling
- Error cases
- Mock implementations

## Example

```javascript
import { render, screen } from '@testing-library/react'
import { MyComponent } from '../components/MyComponent'

test('renders component', () => {
  render(<MyComponent />)
  expect(screen.getByText('Hello')).toBeInTheDocument()
})
```

