from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel, AgentStatus


class DocumentationAgent(BaseAgent):
    """Documentation Agent responsible for creating comprehensive project documentation."""
    
    def __init__(self):
        super().__init__("Technical Writer", "Documentation & User Guides")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create comprehensive documentation for the project."""
        
        self.update_status(AgentStatus.WORKING, 10, "Analyzing documentation requirements")
        
        # Extract all code from previous outputs
        all_code = ""
        frontend_files = []
        backend_files = []
        test_files = []
        
        if previous_outputs and 'generated_files' in previous_outputs:
            for file in previous_outputs['generated_files']:
                content_preview = file['content'][:500] + "..." if len(file['content']) > 500 else file['content']
                all_code += f"\n// {file['path']}\n{content_preview}\n"
                
                if file['type'] == 'frontend':
                    frontend_files.append(file)
                elif file['type'] == 'backend':
                    backend_files.append(file)
                elif file['type'] == 'test':
                    test_files.append(file)
        
        files = []
        
        # Create main README
        readme_file = await self._create_readme(
            project_description, language, design_doc, all_code
        )
        files.append(readme_file)
        
        # Create API documentation
        if backend_files:
            api_docs = await self._create_api_documentation(
                project_description, design_doc, backend_files, language
            )
            files.extend(api_docs)
        
        # Create user guide
        user_guide = await self._create_user_guide(
            project_description, design_doc, frontend_files
        )
        files.append(user_guide)
        
        # Create developer documentation
        dev_docs = await self._create_developer_documentation(
            project_description, language, all_code, design_doc
        )
        files.extend(dev_docs)
        
        # Create deployment guide
        deployment_guide = await self._create_deployment_guide(
            project_description, language, frontend_files, backend_files
        )
        files.append(deployment_guide)
        
        # Create changelog and contributing guidelines
        additional_docs = await self._create_additional_docs(project_description, language)
        files.extend(additional_docs)
        
        self.log(LogLevel.SUCCESS, f"Created {len(files)} documentation files")
        return files
    
    async def _create_readme(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str],
        all_code: str
    ) -> GeneratedFile:
        """Create comprehensive README.md."""
        
        self.update_status(AgentStatus.WORKING, 20, "Creating README.md")
        
        readme_prompt = f"""
        Create a comprehensive README.md for this project:
        
        Project Description: {project_description}
        Primary Language: {language}
        Design Document: {design_doc[:1000] if design_doc else "Not provided"}...
        Code Overview: {all_code[:1500]}...
        
        Create a professional README.md that includes:
        
        1. PROJECT TITLE AND DESCRIPTION
        - Clear, engaging project title
        - Compelling project description
        - Key features and benefits
        - Screenshots or demo links (placeholders)
        
        2. TABLE OF CONTENTS
        
        3. INSTALLATION INSTRUCTIONS
        - Prerequisites and system requirements
        - Step-by-step installation for frontend and backend
        - Environment setup (.env configuration)
        - Database setup if applicable
        
        4. USAGE GUIDE
        - How to start the application
        - Basic usage examples
        - Configuration options
        
        5. PROJECT STRUCTURE
        - Directory structure explanation
        - Key files and their purposes
        
        6. FEATURES
        - Detailed feature list
        - Future planned features
        
        7. TECHNOLOGY STACK
        - Frontend technologies
        - Backend technologies
        - Database and tools
        
        8. CONTRIBUTING
        - How to contribute
        - Code style guidelines
        - Pull request process
        
        9. LICENSE
        - License information
        
        10. CONTACT/SUPPORT
        - How to get help
        - Issue reporting
        
        Make it professional, well-formatted, and easy to follow.
        Use proper Markdown formatting with badges, code blocks, and links.
        """
        
        readme_content = await self._call_llm([
            {"role": "system", "content": "You are an expert technical writer specializing in creating outstanding README files. Write clear, comprehensive documentation."},
            {"role": "user", "content": readme_prompt}
        ])
        
        return GeneratedFile(
            path="README.md",
            content=readme_content,
            type=FileType.DOCUMENTATION
        )
    
    async def _create_api_documentation(
        self,
        project_description: str,
        design_doc: Optional[str],
        backend_files: List[Dict],
        language: str
    ) -> List[GeneratedFile]:
        """Create comprehensive API documentation."""
        
        self.update_status(AgentStatus.WORKING, 40, "Creating API documentation")
        
        files = []
        
        # Create API reference
        api_ref_prompt = f"""
        Create comprehensive API documentation based on the backend code:
        
        Project: {project_description}
        Language: {language}
        Design Document: {design_doc[:1000] if design_doc else "Not provided"}...
        
        Backend Files:
        {chr(10).join([f"- {file['path']}: {file['content'][:300]}..." for file in backend_files[:3]])}
        
        Create API_REFERENCE.md that includes:
        
        1. API OVERVIEW
        - Base URL and versioning
        - Authentication methods
        - Response formats
        - Error handling
        
        2. ENDPOINTS DOCUMENTATION
        For each endpoint:
        - HTTP method and path
        - Description and purpose
        - Request parameters (path, query, body)
        - Request examples (curl, JavaScript, Python)
        - Response examples (success and error)
        - Status codes and their meanings
        
        3. AUTHENTICATION
        - How to authenticate requests
        - Token management
        - Security considerations
        
        4. ERROR HANDLING
        - Error response format
        - Common error codes
        - Troubleshooting guide
        
        5. RATE LIMITING
        - Rate limit information
        - Headers and responses
        
        6. SDKs AND LIBRARIES
        - Available client libraries
        - Usage examples
        
        Make it comprehensive and developer-friendly with lots of examples.
        """
        
        api_ref_content = await self._call_llm([
            {"role": "system", "content": "You are an expert API documentation writer. Create clear, comprehensive API docs with examples."},
            {"role": "user", "content": api_ref_prompt}
        ])
        
        files.append(GeneratedFile(
            path="docs/API_REFERENCE.md",
            content=api_ref_content,
            type=FileType.DOCUMENTATION
        ))
        
        # Create OpenAPI/Swagger spec if applicable
        if language == "Python" or "fastapi" in str(backend_files).lower():
            openapi_prompt = f"""
            Create an OpenAPI 3.0 specification (YAML format) for the API based on:
            
            Project: {project_description}
            Backend Files: {chr(10).join([f"- {file['path']}" for file in backend_files[:3]])}
            
            Create openapi.yaml with:
            1. Complete OpenAPI 3.0 spec
            2. All endpoints with full documentation
            3. Request/response schemas
            4. Authentication schemes
            5. Examples for all operations
            6. Proper tags and descriptions
            
            Make it valid OpenAPI 3.0 YAML.
            """
            
            openapi_content = await self._call_llm([
                {"role": "system", "content": "You are an expert in OpenAPI specification. Create valid, comprehensive OpenAPI 3.0 YAML."},
                {"role": "user", "content": openapi_prompt}
            ])
            
            files.append(GeneratedFile(
                path="docs/openapi.yaml",
                content=openapi_content,
                type=FileType.DOCUMENTATION
            ))
        
        return files
    
    async def _create_user_guide(
        self,
        project_description: str,
        design_doc: Optional[str],
        frontend_files: List[Dict]
    ) -> GeneratedFile:
        """Create user guide for the application."""
        
        self.update_status(AgentStatus.WORKING, 60, "Creating user guide")
        
        user_guide_prompt = f"""
        Create a comprehensive user guide for end users:
        
        Project: {project_description}
        Design Document: {design_doc[:1000] if design_doc else "Not provided"}...
        Frontend Overview: {chr(10).join([f"- {file['path']}" for file in frontend_files[:3]])}
        
        Create USER_GUIDE.md that includes:
        
        1. GETTING STARTED
        - Account setup (if applicable)
        - First-time user walkthrough
        - Interface overview
        
        2. CORE FEATURES
        - Step-by-step guides for each major feature
        - Screenshots and examples (placeholders)
        - Tips and best practices
        
        3. COMMON WORKFLOWS
        - Typical user scenarios
        - End-to-end workflows
        - Integration with other tools
        
        4. TROUBLESHOOTING
        - Common issues and solutions
        - FAQ section
        - Error messages and fixes
        
        5. ADVANCED FEATURES
        - Power user features
        - Customization options
        - Automation possibilities
        
        6. SUPPORT
        - How to get help
        - Contact information
        - Community resources
        
        Write in a friendly, accessible tone for non-technical users.
        Include placeholders for screenshots and videos.
        """
        
        user_guide_content = await self._call_llm([
            {"role": "system", "content": "You are an expert technical writer specializing in user-friendly documentation. Write clear, accessible guides for end users."},
            {"role": "user", "content": user_guide_prompt}
        ])
        
        return GeneratedFile(
            path="docs/USER_GUIDE.md",
            content=user_guide_content,
            type=FileType.DOCUMENTATION
        )
    
    async def _create_developer_documentation(
        self,
        project_description: str,
        language: str,
        all_code: str,
        design_doc: Optional[str]
    ) -> List[GeneratedFile]:
        """Create developer-focused documentation."""
        
        self.update_status(AgentStatus.WORKING, 75, "Creating developer documentation")
        
        files = []
        
        # Create architecture documentation
        architecture_prompt = f"""
        Create detailed architecture documentation:
        
        Project: {project_description}
        Language: {language}
        Design Document: {design_doc[:1000] if design_doc else "Not provided"}...
        Code Overview: {all_code[:1000]}...
        
        Create ARCHITECTURE.md that includes:
        
        1. SYSTEM OVERVIEW
        - High-level architecture diagram (ASCII art or description)
        - Component relationships
        - Data flow diagrams
        
        2. FRONTEND ARCHITECTURE
        - Component hierarchy
        - State management approach
        - Routing structure
        - Build process
        
        3. BACKEND ARCHITECTURE
        - Service layer organization
        - Database design
        - API design patterns
        - Authentication flow
        
        4. INFRASTRUCTURE
        - Deployment architecture
        - Scaling considerations
        - Performance optimizations
        
        5. DESIGN DECISIONS
        - Technology choices and rationale
        - Trade-offs made
        - Alternative approaches considered
        
        6. FUTURE IMPROVEMENTS
        - Planned enhancements
        - Technical debt areas
        - Refactoring opportunities
        
        Make it technical but accessible to developers joining the project.
        """
        
        architecture_content = await self._call_llm([
            {"role": "system", "content": "You are a senior software architect. Create comprehensive architecture documentation for developers."},
            {"role": "user", "content": architecture_prompt}
        ])
        
        files.append(GeneratedFile(
            path="docs/ARCHITECTURE.md",
            content=architecture_content,
            type=FileType.DOCUMENTATION
        ))
        
        # Create development setup guide
        dev_setup_prompt = f"""
        Create a developer setup guide:
        
        Project: {project_description}
        Language: {language}
        
        Create DEVELOPMENT.md that includes:
        
        1. PREREQUISITES
        - Required software and versions
        - System requirements
        - Account setups needed
        
        2. LOCAL DEVELOPMENT SETUP
        - Repository cloning
        - Environment configuration
        - Database setup
        - Service dependencies
        
        3. DEVELOPMENT WORKFLOW
        - Branch naming conventions
        - Commit message format
        - Code review process
        - Testing requirements
        
        4. DEBUGGING
        - Debug configuration
        - Logging setup
        - Common debugging scenarios
        
        5. TOOLS AND UTILITIES
        - Recommended IDE setup
        - Useful extensions/plugins
        - Development scripts
        
        6. PERFORMANCE PROFILING
        - How to profile the application
        - Performance monitoring tools
        
        Make it comprehensive for new developers joining the team.
        """
        
        dev_setup_content = await self._call_llm([
            {"role": "system", "content": "You are an expert in developer experience. Create comprehensive development setup guides."},
            {"role": "user", "content": dev_setup_prompt}
        ])
        
        files.append(GeneratedFile(
            path="docs/DEVELOPMENT.md",
            content=dev_setup_content,
            type=FileType.DOCUMENTATION
        ))
        
        return files
    
    async def _create_deployment_guide(
        self,
        project_description: str,
        language: str,
        frontend_files: List[Dict],
        backend_files: List[Dict]
    ) -> GeneratedFile:
        """Create deployment documentation."""
        
        self.update_status(AgentStatus.WORKING, 85, "Creating deployment guide")
        
        deployment_prompt = f"""
        Create comprehensive deployment documentation:
        
        Project: {project_description}
        Language: {language}
        Has Frontend: {len(frontend_files) > 0}
        Has Backend: {len(backend_files) > 0}
        
        Create DEPLOYMENT.md that includes:
        
        1. DEPLOYMENT OPTIONS
        - Local deployment
        - Cloud deployment (AWS, GCP, Azure)
        - Container deployment (Docker)
        - Serverless options
        
        2. ENVIRONMENT CONFIGURATION
        - Environment variables
        - Configuration files
        - Secrets management
        
        3. DATABASE SETUP
        - Database creation and migration
        - Connection configuration
        - Backup strategies
        
        4. FRONTEND DEPLOYMENT
        - Build process
        - Static file serving
        - CDN configuration
        - Domain setup
        
        5. BACKEND DEPLOYMENT
        - Server configuration
        - Process management
        - Load balancing
        - Health checks
        
        6. MONITORING AND LOGGING
        - Application monitoring
        - Error tracking
        - Performance monitoring
        - Log aggregation
        
        7. SECURITY CONSIDERATIONS
        - SSL/TLS setup
        - Security headers
        - Access controls
        - Vulnerability scanning
        
        8. MAINTENANCE
        - Update procedures
        - Backup and restore
        - Disaster recovery
        
        Provide specific examples for popular platforms.
        """
        
        deployment_content = await self._call_llm([
            {"role": "system", "content": "You are a DevOps expert. Create comprehensive, practical deployment guides with specific examples."},
            {"role": "user", "content": deployment_prompt}
        ])
        
        return GeneratedFile(
            path="docs/DEPLOYMENT.md",
            content=deployment_content,
            type=FileType.DOCUMENTATION
        )
    
    async def _create_additional_docs(self, project_description: str, language: str) -> List[GeneratedFile]:
        """Create additional documentation files."""
        
        self.update_status(AgentStatus.WORKING, 95, "Creating additional documentation")
        
        files = []
        
        # Create CHANGELOG.md
        changelog_content = f"""# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - {self._get_current_date()}

### Added
- Initial release of {project_description}
- Complete {language} implementation
- Comprehensive test suite
- Full documentation
- Deployment guides

### Security
- Implemented security best practices
- Added input validation
- Secure configuration defaults

"""
        
        files.append(GeneratedFile(
            path="CHANGELOG.md",
            content=changelog_content,
            type=FileType.DOCUMENTATION
        ))
        
        # Create CONTRIBUTING.md
        contributing_content = f"""# Contributing to {project_description}

We love your input! We want to make contributing to this project as easy and transparent as possible.

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Request Process

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Coding Standards

### {language} Style Guide
- Follow the established patterns in the codebase
- Use meaningful variable and function names
- Add comments for complex logic
- Write tests for new features

### Commit Messages
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

## Testing

- Write unit tests for new functionality
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage
- Test edge cases and error conditions

## Documentation

- Update README.md if needed
- Document new APIs in the API reference
- Add inline code comments for complex logic
- Update user guides for new features

## Issue Reporting

We use GitHub issues to track public bugs. Report a bug by opening a new issue.

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening)

## License

By contributing, you agree that your contributions will be licensed under the project license.

## Questions?

Don't hesitate to contact the maintainers if you have questions!
"""
        
        files.append(GeneratedFile(
            path="CONTRIBUTING.md",
            content=contributing_content,
            type=FileType.DOCUMENTATION
        ))
        
        # Create LICENSE file
        license_content = """MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
        
        files.append(GeneratedFile(
            path="LICENSE",
            content=license_content,
            type=FileType.DOCUMENTATION
        ))
        
        return files
    
    def _get_current_date(self) -> str:
        """Get current date in YYYY-MM-DD format."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
