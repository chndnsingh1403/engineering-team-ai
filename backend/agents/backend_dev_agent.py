import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel, AgentStatus


class BackendDevAgent(BaseAgent):
    """Backend Developer Agent responsible for creating the backend API."""
    
    def __init__(self):
        super().__init__("Backend Developer", "API Development & Backend Services")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create backend application based on design document."""
        
        self.log(LogLevel.INFO, "⚙️ Backend Developer starting API development")
        self.update_status(AgentStatus.WORKING, 10, "Analyzing backend requirements")
        await asyncio.sleep(1)
        
        self.log(LogLevel.INFO, "🔧 Designing RESTful API architecture")
        self.update_progress(25, "Creating API structure")
        await asyncio.sleep(1)
        
        # Determine backend framework based on language
        framework_map = {
            "Python": "FastAPI",
            "JavaScript/TypeScript": "Node.js with Express",
            "Java": "Spring Boot",
            "C#": "ASP.NET Core",
            "Go": "Gin or Fiber",
            "Rust": "Actix-web",
            "PHP": "Laravel",
            "Ruby": "Ruby on Rails"
        }
        
        framework = framework_map.get(language, "FastAPI")
        
        backend_prompt = f"""
        As a Senior Backend Developer, create a complete backend API using {framework} for {language}.
        
        Project Description: {project_description}
        Framework: {framework}
        Design Document: {design_doc if design_doc else "Create based on project description"}
        
        Create a production-ready backend API with:
        
        1. API STRUCTURE
        - RESTful API endpoints
        - Request/response models
        - Input validation
        - Error handling
        
        2. DATA LAYER
        - Database models/schemas
        - Database connection setup
        - Migration scripts (if applicable)
        
        3. BUSINESS LOGIC
        - Service layer implementation
        - Core business logic
        - Data processing functions
        
        4. SECURITY
        - Authentication setup
        - Authorization middleware
        - Input sanitization
        - CORS configuration
        
        5. CONFIGURATION
        - Environment configuration
        - Logging setup
        - Health check endpoints
        
        Please provide complete, working code for all components.
        """
        
        self.update_status(AgentStatus.WORKING, 30, "Creating API structure")
        
        backend_code = await self.call_openai([
            {"role": "system", "content": f"You are a senior backend developer expert in {framework} and {language}."},
            {"role": "user", "content": backend_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 50, "Implementing core services")
        
        # Generate specific backend components
        services_prompt = f"""
        Create detailed implementation for the backend services:
        
        Project: {project_description}
        Framework: {framework}
        
        Generate these specific files with complete implementation:
        
        1. main.py/app.py - Application entry point
        2. models.py - Data models and schemas
        3. database.py - Database connection and setup
        4. routes/api.py - API route definitions
        5. services/ - Business logic services
        6. middleware/ - Custom middleware
        7. utils/ - Utility functions
        8. config.py - Configuration management
        
        Each file should be:
        - Production-ready
        - Well-documented
        - Include error handling
        - Follow best practices
        - Include proper logging
        """
        
        services_code = await self.call_openai([
            {"role": "system", "content": f"You are an expert {language} backend developer creating scalable applications."},
            {"role": "user", "content": services_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 70, "Creating configuration files")
        
        # Generate configuration and deployment files
        config_prompt = f"""
        Create configuration and deployment files for the {framework} backend:
        
        1. requirements.txt / package.json - Dependencies
        2. .env.example - Environment variables
        3. Dockerfile - Container configuration
        4. docker-compose.yml - Multi-service setup
        5. README.md - Setup and deployment instructions
        6. .gitignore - Git ignore rules
        7. pytest.ini / jest.config.js - Testing configuration
        8. alembic.ini - Database migration config (if applicable)
        
        Include proper documentation and setup instructions.
        """
        
        config_files = await self.call_openai([
            {"role": "system", "content": "You are a DevOps engineer expert in backend deployment and configuration."},
            {"role": "user", "content": config_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 90, "Finalizing backend structure")
        
        # Create API documentation
        docs_prompt = f"""
        Create comprehensive API documentation for the backend:
        
        Framework: {framework}
        Project: {project_description}
        
        Generate:
        1. API_DOCUMENTATION.md - Complete API reference
        2. DEPLOYMENT_GUIDE.md - Deployment instructions
        3. DEVELOPMENT_SETUP.md - Local development setup
        
        Include:
        - All endpoint documentation
        - Request/response examples
        - Authentication details
        - Error codes and handling
        - Environment setup
        """
        
        documentation = await self.call_openai([
            {"role": "system", "content": "You are a technical writer specializing in API documentation."},
            {"role": "user", "content": docs_prompt}
        ])
        
        # Generate files based on language/framework
        files = self._generate_backend_files(
            language, framework, backend_code, services_code, 
            config_files, documentation
        )
        
        self.log(LogLevel.SUCCESS, f"Generated {len(files)} backend files")
        return files
    
    def _generate_backend_files(
        self, 
        language: str, 
        framework: str, 
        backend_code: str,
        services_code: str,
        config_files: str,
        documentation: str
    ) -> List[GeneratedFile]:
        """Generate backend files based on language and framework."""
        files = []
        
        if language == "Python" or framework == "FastAPI":
            files.extend([
                GeneratedFile(
                    path="backend/main.py",
                    content=self._extract_file_content(backend_code, "main.py"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/models.py",
                    content=self._extract_file_content(services_code, "models.py"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/database.py",
                    content=self._extract_file_content(services_code, "database.py"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/routes/api.py",
                    content=self._extract_file_content(services_code, "routes"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/services/main_service.py",
                    content=self._extract_file_content(services_code, "services"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/config.py",
                    content=self._extract_file_content(services_code, "config.py"),
                    type=FileType.BACKEND
                ),
                GeneratedFile(
                    path="backend/requirements.txt",
                    content=self._extract_file_content(config_files, "requirements.txt"),
                    type=FileType.BACKEND
                )
            ])
        
        # Add common files regardless of language
        files.extend([
            GeneratedFile(
                path="backend/.env.example",
                content=self._extract_file_content(config_files, ".env.example"),
                type=FileType.BACKEND
            ),
            GeneratedFile(
                path="backend/Dockerfile",
                content=self._extract_file_content(config_files, "Dockerfile"),
                type=FileType.BACKEND
            ),
            GeneratedFile(
                path="backend/docker-compose.yml",
                content=self._extract_file_content(config_files, "docker-compose.yml"),
                type=FileType.BACKEND
            ),
            GeneratedFile(
                path="backend/README.md",
                content=self._extract_file_content(config_files, "README.md"),
                type=FileType.BACKEND
            ),
            GeneratedFile(
                path="backend/.gitignore",
                content=self._extract_file_content(config_files, ".gitignore"),
                type=FileType.BACKEND
            ),
            GeneratedFile(
                path="docs/API_DOCUMENTATION.md",
                content=self._extract_file_content(documentation, "API_DOCUMENTATION.md"),
                type=FileType.DOCUMENTATION
            ),
            GeneratedFile(
                path="docs/DEPLOYMENT_GUIDE.md",
                content=self._extract_file_content(documentation, "DEPLOYMENT_GUIDE.md"),
                type=FileType.DOCUMENTATION
            )
        ])
        
        return files
    
    def _extract_file_content(self, content: str, filename: str) -> str:
        """Extract specific file content from AI response."""
        # Simple extraction logic - in production, you'd want more sophisticated parsing
        lines = content.split('\n')
        in_file = False
        file_lines = []
        
        for line in lines:
            if filename in line and ('```' in line or 'py' in line or 'js' in line):
                in_file = True
                continue
            if in_file and '```' in line:
                break
            if in_file:
                file_lines.append(line)
        
        if file_lines:
            return '\n'.join(file_lines)
        
        # Fallback content based on file type
        fallbacks = {
            "main.py": """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Generated API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Generated API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
""",
            "requirements.txt": """fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
python-multipart==0.0.6
python-dotenv==1.0.0
""",
            "README.md": f"""# Generated Backend API

This backend API was auto-generated by the Engineering Team AI.

## Setup

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start server:
   ```bash
   uvicorn main:app --reload
   ```

The API will be available at http://localhost:8000
"""
        }
        
        return fallbacks.get(filename.split('/')[-1], f"# Generated {filename}\n# Auto-generated by Engineering Team AI")
