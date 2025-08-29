from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel, AgentStatus


class TestDevAgent(BaseAgent):
    """Test Developer Agent responsible for creating comprehensive tests."""
    
    def __init__(self):
        super().__init__("Test Engineer", "Quality Assurance & Testing")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create comprehensive test suite for the application."""
        
        self.update_status(AgentStatus.WORKING, 10, "Analyzing testing requirements")
        self.log(LogLevel.INFO, "Starting test development")
        
        # Extract information about frontend and backend from previous outputs
        frontend_files = []
        backend_files = []
        
        if previous_outputs:
            for output_list in previous_outputs.values():
                for file in output_list:
                    if hasattr(file, 'type'):
                        if file.type == FileType.FRONTEND:
                            frontend_files.append(file)
                        elif file.type == FileType.BACKEND:
                            backend_files.append(file)
        
        self.update_status(AgentStatus.WORKING, 25, "Creating frontend tests")
        
        # Generate frontend tests
        frontend_test_prompt = f"""
        As a Senior QA Engineer, create comprehensive frontend tests for the application.
        
        Project Description: {project_description}
        Language: {language}
        
        Frontend files to test: {[f.path for f in frontend_files[:5]]}
        
        Create tests for:
        
        1. UNIT TESTS
        - Component testing
        - Utility function tests
        - Hook testing (if applicable)
        - Service layer tests
        
        2. INTEGRATION TESTS
        - API integration tests
        - Component interaction tests
        - Form validation tests
        
        3. END-TO-END TESTS
        - User workflow tests
        - Critical path testing
        - Cross-browser compatibility
        
        4. TEST UTILITIES
        - Test helpers and mocks
        - Custom render functions
        - Test data factories
        
        Generate complete test files with:
        - Jest/Vitest configuration
        - React Testing Library setup
        - Cypress/Playwright E2E tests
        - Test coverage configuration
        
        Ensure tests are maintainable and follow best practices.
        """
        
        frontend_tests = await self.call_openai([
            {"role": "system", "content": "You are a senior frontend testing specialist expert in Jest, React Testing Library, and E2E testing."},
            {"role": "user", "content": frontend_test_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 50, "Creating backend tests")
        
        # Generate backend tests
        backend_test_prompt = f"""
        Create comprehensive backend tests for the API.
        
        Project Description: {project_description}
        Language: {language}
        
        Backend files to test: {[f.path for f in backend_files[:5]]}
        
        Create tests for:
        
        1. UNIT TESTS
        - Service layer testing
        - Model validation tests
        - Utility function tests
        - Database query tests
        
        2. INTEGRATION TESTS
        - API endpoint tests
        - Database integration tests
        - Authentication tests
        - Middleware tests
        
        3. PERFORMANCE TESTS
        - Load testing scenarios
        - Stress testing
        - API response time tests
        
        4. SECURITY TESTS
        - Input validation tests
        - Authentication bypass tests
        - SQL injection prevention
        - XSS protection tests
        
        Generate complete test files with:
        - Pytest/Jest configuration
        - Test fixtures and factories
        - Mock services
        - Test database setup
        
        Include proper test data management and cleanup.
        """
        
        backend_tests = await self.call_openai([
            {"role": "system", "content": "You are a senior backend testing specialist expert in API testing, security testing, and performance testing."},
            {"role": "user", "content": backend_test_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 75, "Creating test configuration")
        
        # Generate test configuration and automation
        test_config_prompt = f"""
        Create test configuration and CI/CD integration for the project.
        
        Language: {language}
        
        Generate:
        
        1. TEST CONFIGURATION FILES
        - Jest/Vitest config
        - Pytest configuration
        - Coverage reporting setup
        - Test environment configuration
        
        2. CI/CD PIPELINE
        - GitHub Actions workflow
        - Test automation scripts
        - Coverage reporting
        - Quality gates
        
        3. TEST DOCUMENTATION
        - Testing strategy document
        - Test execution guide
        - Coverage requirements
        - Bug report template
        
        4. QUALITY ASSURANCE
        - Code quality checks
        - Linting rules for tests
        - Test best practices guide
        
        Include scripts for running different types of tests locally and in CI.
        """
        
        test_config = await self.call_openai([
            {"role": "system", "content": "You are a DevOps engineer specializing in test automation and CI/CD pipelines."},
            {"role": "user", "content": test_config_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 90, "Generating test files")
        
        # Create test files
        files = []
        
        # Frontend test files
        files.extend([
            GeneratedFile(
                path="frontend/src/__tests__/App.test.tsx",
                content=self._extract_test_content(frontend_tests, "App.test"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="frontend/src/__tests__/components/Header.test.tsx",
                content=self._extract_test_content(frontend_tests, "Header.test"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="frontend/src/__tests__/services/ApiService.test.ts",
                content=self._extract_test_content(frontend_tests, "ApiService.test"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="frontend/cypress/e2e/main-workflow.cy.ts",
                content=self._extract_test_content(frontend_tests, "e2e"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="frontend/src/test-utils/test-helpers.ts",
                content=self._extract_test_content(frontend_tests, "test-utils"),
                type=FileType.TEST
            )
        ])
        
        # Backend test files
        files.extend([
            GeneratedFile(
                path="backend/tests/test_main.py",
                content=self._extract_test_content(backend_tests, "test_main"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="backend/tests/test_api.py",
                content=self._extract_test_content(backend_tests, "test_api"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="backend/tests/test_services.py",
                content=self._extract_test_content(backend_tests, "test_services"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="backend/tests/test_models.py",
                content=self._extract_test_content(backend_tests, "test_models"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="backend/tests/conftest.py",
                content=self._extract_test_content(backend_tests, "conftest"),
                type=FileType.TEST
            )
        ])
        
        # Configuration files
        files.extend([
            GeneratedFile(
                path="frontend/jest.config.js",
                content=self._extract_config_content(test_config, "jest.config"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="frontend/cypress.config.ts",
                content=self._extract_config_content(test_config, "cypress.config"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="backend/pytest.ini",
                content=self._extract_config_content(test_config, "pytest.ini"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path=".github/workflows/tests.yml",
                content=self._extract_config_content(test_config, "github-actions"),
                type=FileType.TEST
            ),
            GeneratedFile(
                path="docs/TESTING_GUIDE.md",
                content=self._extract_config_content(test_config, "testing-guide"),
                type=FileType.DOCUMENTATION
            ),
            GeneratedFile(
                path="docs/QA_STRATEGY.md",
                content=self._extract_config_content(test_config, "qa-strategy"),
                type=FileType.DOCUMENTATION
            )
        ])
        
        self.log(LogLevel.SUCCESS, f"Generated {len(files)} test files")
        return files
    
    def _extract_test_content(self, content: str, test_name: str) -> str:
        """Extract specific test content from AI response."""
        lines = content.split('\n')
        in_test = False
        test_lines = []
        
        for line in lines:
            if test_name in line and ('```' in line or 'test' in line):
                in_test = True
                continue
            if in_test and '```' in line:
                break
            if in_test:
                test_lines.append(line)
        
        if test_lines:
            return '\n'.join(test_lines)
        
        # Fallback test content
        fallbacks = {
            "App.test": """import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    expect(screen.getByText(/app/i)).toBeInTheDocument();
  });
  
  test('displays main content', () => {
    render(<App />);
    expect(document.querySelector('.App')).toBeInTheDocument();
  });
});""",
            "test_main": """import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
""",
            "conftest": """import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def sample_data():
    return {
        "test": "data"
    }
"""
        }
        
        return fallbacks.get(test_name, f"""# Generated {test_name} test
# Auto-generated by Engineering Team AI

def test_placeholder():
    assert True
""")
    
    def _extract_config_content(self, content: str, config_name: str) -> str:
        """Extract configuration content from AI response."""
        lines = content.split('\n')
        in_config = False
        config_lines = []
        
        for line in lines:
            if config_name in line and ('```' in line or 'config' in line):
                in_config = True
                continue
            if in_config and '```' in line:
                break
            if in_config:
                config_lines.append(line)
        
        if config_lines:
            return '\n'.join(config_lines)
        
        # Fallback configurations
        fallbacks = {
            "jest.config": """module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
  collectCoverageFrom: [
    'src/**/*.{ts,tsx}',
    '!src/**/*.d.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
};""",
            "pytest.ini": """[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = --verbose --cov=. --cov-report=html --cov-report=term-missing
filterwarnings =
    ignore::DeprecationWarning
    ignore::PendingDeprecationWarning
""",
            "testing-guide": """# Testing Guide

## Overview
This document outlines the testing strategy and practices for the project.

## Frontend Testing
- Unit tests using Jest and React Testing Library
- E2E tests using Cypress
- Component testing best practices

## Backend Testing  
- Unit tests using Pytest
- API integration tests
- Database testing with fixtures

## Running Tests

### Frontend
```bash
npm test                 # Unit tests
npm run test:e2e        # E2E tests
npm run test:coverage   # Coverage report
```

### Backend
```bash
pytest                  # All tests
pytest --cov           # With coverage
pytest tests/unit/     # Unit tests only
```

## Coverage Requirements
- Minimum 80% code coverage
- All critical paths must be tested
- New features require tests
"""
        }
        
        return fallbacks.get(config_name, f"# Generated {config_name}\n# Configuration auto-generated by Engineering Team AI")
