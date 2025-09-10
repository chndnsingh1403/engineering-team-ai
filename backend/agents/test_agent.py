from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel


class TestAgent(BaseAgent):
    """Test Development Agent responsible for creating comprehensive tests."""
    
    def __init__(self):
        super().__init__("Test Engineer", "Test Development & Quality Assurance")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create comprehensive test suites for frontend and backend."""
        
        self.update_status(self.agent.status, 10, "Analyzing testing requirements")
        
        if not design_doc:
            raise ValueError("Design document is required for test development")
        
        # Extract frontend and backend code from previous outputs
        frontend_code = ""
        backend_code = ""
        
        if previous_outputs and 'generated_files' in previous_outputs:
            for file in previous_outputs['generated_files']:
                if file['type'] == 'frontend':
                    frontend_code += f"\n// {file['path']}\n{file['content']}\n"
                elif file['type'] == 'backend':
                    backend_code += f"\n// {file['path']}\n{file['content']}\n"
        
        files = []
        
        # Create backend tests
        if backend_code or language:
            backend_tests = await self._create_backend_tests(
                project_description, design_doc, language, backend_code
            )
            files.extend(backend_tests)
        
        # Create frontend tests
        if frontend_code or language:
            frontend_tests = await self._create_frontend_tests(
                project_description, design_doc, language, frontend_code
            )
            files.extend(frontend_tests)
        
        # Create integration tests
        integration_tests = await self._create_integration_tests(
            project_description, design_doc, language
        )
        files.extend(integration_tests)
        
        # Create test configuration and documentation
        config_files = await self._create_test_config(language)
        files.extend(config_files)
        
        self.log(LogLevel.SUCCESS, f"Created {len(files)} test files")
        return files
    
    async def _create_backend_tests(
        self, 
        project_description: str, 
        design_doc: str, 
        language: str,
        backend_code: str
    ) -> List[GeneratedFile]:
        """Create backend test files."""
        files = []
        
        self.update_status(self.agent.status, 25, "Creating backend unit tests")
        
        if language == "Python":
            # Create pytest tests
            backend_test_prompt = f"""
            Create comprehensive pytest test suite for the backend code.
            
            Project: {project_description}
            Design Document: {design_doc}
            Backend Code: {backend_code[:2000]}...
            
            Create test_main.py with:
            1. Unit tests for all API endpoints
            2. Test fixtures and mocks
            3. Database testing (if applicable)
            4. Authentication testing (if applicable)
            5. File upload testing (if applicable)
            6. Error handling tests
            7. Edge case testing
            8. Performance tests for critical paths
            9. Proper test isolation
            10. Test data factories
            
            Use pytest, pytest-asyncio, httpx for FastAPI testing.
            Follow testing best practices.
            """
            
            backend_test_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in Python testing with pytest. Write comprehensive, maintainable tests."},
                {"role": "user", "content": backend_test_prompt}
            ])
            
            files.append(GeneratedFile(
                path="tests/test_backend.py",
                content=backend_test_content,
                type=FileType.TEST
            ))
            
            # Create conftest.py for shared fixtures
            conftest_prompt = f"""
            Create conftest.py with shared pytest fixtures for:
            
            Project: {project_description}
            Backend Code: {backend_code[:1000]}...
            
            Include fixtures for:
            1. Test client setup
            2. Database setup/teardown
            3. Mock external services
            4. Test data factories
            5. Authentication fixtures
            6. File upload mocks
            
            Make fixtures reusable across test modules.
            """
            
            conftest_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in pytest fixture design. Create efficient, reusable fixtures."},
                {"role": "user", "content": conftest_prompt}
            ])
            
            files.append(GeneratedFile(
                path="tests/conftest.py",
                content=conftest_content,
                type=FileType.TEST
            ))
            
        elif language in ["JavaScript/TypeScript", "JavaScript", "TypeScript"]:
            # Create Jest tests for Node.js
            js_test_prompt = f"""
            Create comprehensive Jest test suite for the Node.js backend.
            
            Project: {project_description}
            Design Document: {design_doc}
            Backend Code: {backend_code[:2000]}...
            
            Create test files with:
            1. Unit tests for all routes
            2. Integration tests
            3. Mock external dependencies
            4. Authentication testing
            5. File upload testing
            6. Error handling tests
            7. Database testing (if applicable)
            8. WebSocket testing (if applicable)
            
            Use Jest, supertest, and appropriate mocking libraries.
            """
            
            js_test_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in JavaScript/TypeScript testing with Jest. Write thorough test suites."},
                {"role": "user", "content": js_test_prompt}
            ])
            
            files.append(GeneratedFile(
                path="tests/backend.test.js",
                content=js_test_content,
                type=FileType.TEST
            ))
        
        return files
    
    async def _create_frontend_tests(
        self,
        project_description: str,
        design_doc: str,
        language: str,
        frontend_code: str
    ) -> List[GeneratedFile]:
        """Create frontend test files."""
        files = []
        
        self.update_status(self.agent.status, 50, "Creating frontend tests")
        
        if language in ["JavaScript/TypeScript", "JavaScript", "TypeScript"]:
            # Create React Testing Library tests
            frontend_test_prompt = f"""
            Create comprehensive React Testing Library test suite for the frontend.
            
            Project: {project_description}
            Design Document: {design_doc}
            Frontend Code: {frontend_code[:2000]}...
            
            Create component tests that include:
            1. Unit tests for all components
            2. User interaction testing
            3. Form validation testing
            4. API integration testing with mocks
            5. Accessibility testing
            6. Error state testing
            7. Loading state testing
            8. Responsive design testing
            9. Integration tests for user flows
            10. Snapshot testing for UI consistency
            
            Use React Testing Library, Jest, MSW for API mocking.
            Follow testing best practices for React applications.
            """
            
            frontend_test_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in React testing with Testing Library. Write user-focused, maintainable tests."},
                {"role": "user", "content": frontend_test_prompt}
            ])
            
            files.append(GeneratedFile(
                path="frontend/src/__tests__/App.test.tsx",
                content=frontend_test_content,
                type=FileType.TEST
            ))
            
            # Create test utilities
            test_utils_prompt = f"""
            Create test utilities and setup files for React testing:
            
            Project: {project_description}
            
            Create test-utils.tsx with:
            1. Custom render function with providers
            2. Mock setup utilities
            3. Test data factories
            4. Common assertions helpers
            5. API mocking setup
            6. Router testing utilities
            
            Make testing more efficient and consistent.
            """
            
            test_utils_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in React testing utilities. Create reusable testing helpers."},
                {"role": "user", "content": test_utils_prompt}
            ])
            
            files.append(GeneratedFile(
                path="frontend/src/test-utils.tsx",
                content=test_utils_content,
                type=FileType.TEST
            ))
            
        elif language == "Python":
            # Create Streamlit tests
            streamlit_test_prompt = f"""
            Create tests for Streamlit application:
            
            Project: {project_description}
            Frontend Code: {frontend_code[:1000]}...
            
            Create test_streamlit_app.py with:
            1. Component testing
            2. Session state testing
            3. User interaction simulation
            4. API integration testing
            5. File upload testing
            
            Use appropriate Streamlit testing approaches.
            """
            
            streamlit_test_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in Streamlit application testing."},
                {"role": "user", "content": streamlit_test_prompt}
            ])
            
            files.append(GeneratedFile(
                path="tests/test_frontend.py",
                content=streamlit_test_content,
                type=FileType.TEST
            ))
        
        return files
    
    async def _create_integration_tests(
        self,
        project_description: str,
        design_doc: str,
        language: str
    ) -> List[GeneratedFile]:
        """Create end-to-end integration tests."""
        files = []
        
        self.update_status(self.agent.status, 75, "Creating integration tests")
        
        # Create E2E tests
        e2e_test_prompt = f"""
        Create end-to-end integration tests for the full application:
        
        Project: {project_description}
        Design Document: {design_doc}
        Language: {language}
        
        Create integration test suite that includes:
        1. Full user workflow testing
        2. Frontend-backend integration
        3. API contract testing
        4. File upload end-to-end testing
        5. Error scenario testing
        6. Performance testing
        7. Database integration testing (if applicable)
        8. Authentication flow testing (if applicable)
        
        Use appropriate tools like Playwright, Cypress, or Selenium.
        Focus on critical user journeys.
        """
        
        e2e_content = await self._call_llm([
            {"role": "system", "content": "You are an expert in end-to-end testing. Create comprehensive integration tests."},
            {"role": "user", "content": e2e_test_prompt}
        ])
        
        files.append(GeneratedFile(
            path="tests/test_integration.py" if language == "Python" else "tests/integration.test.js",
            content=e2e_content,
            type=FileType.TEST
        ))
        
        return files
    
    async def _create_test_config(self, language: str) -> List[GeneratedFile]:
        """Create test configuration files."""
        files = []
        
        self.update_status(self.agent.status, 90, "Creating test configuration")
        
        if language == "Python":
            # Create pytest.ini
            pytest_config = """
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=.
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
    api: API tests
"""
            
            files.append(GeneratedFile(
                path="pytest.ini",
                content=pytest_config,
                type=FileType.TEST
            ))
            
            # Create test requirements
            test_requirements = """
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
httpx>=0.25.0
pytest-mock>=3.11.0
factory-boy>=3.3.0
"""
            
            files.append(GeneratedFile(
                path="test-requirements.txt",
                content=test_requirements,
                type=FileType.TEST
            ))
            
        elif language in ["JavaScript/TypeScript", "JavaScript", "TypeScript"]:
            # Create Jest config
            jest_config = {
                "testEnvironment": "jsdom",
                "setupFilesAfterEnv": ["<rootDir>/src/setupTests.js"],
                "moduleNameMapping": {
                    "^@/(.*)$": "<rootDir>/src/$1"
                },
                "collectCoverageFrom": [
                    "src/**/*.{js,jsx,ts,tsx}",
                    "!src/**/*.d.ts",
                    "!src/main.tsx",
                    "!src/vite-env.d.ts"
                ],
                "coverageThreshold": {
                    "global": {
                        "branches": 80,
                        "functions": 80,
                        "lines": 80,
                        "statements": 80
                    }
                }
            }
            
            files.append(GeneratedFile(
                path="frontend/jest.config.js",
                content=f"module.exports = {jest_config}",
                type=FileType.TEST
            ))
            
        # Create test documentation
        test_docs_prompt = f"""
        Create comprehensive testing documentation for {language} project:
        
        Create TESTING.md that includes:
        1. Testing strategy overview
        2. How to run different types of tests
        3. Writing new tests guidelines
        4. Test coverage requirements
        5. Debugging failing tests
        6. Continuous integration setup
        7. Performance testing guidelines
        8. Best practices for maintainable tests
        
        Make it clear and actionable for developers.
        """
        
        test_docs_content = await self._call_llm([
            {"role": "system", "content": "You are an expert in software testing documentation. Create clear, comprehensive guides."},
            {"role": "user", "content": test_docs_prompt}
        ])
        
        files.append(GeneratedFile(
            path="TESTING.md",
            content=test_docs_content,
            type=FileType.TEST
        ))
        
        return files
