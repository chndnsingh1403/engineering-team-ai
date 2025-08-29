import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel


class BackendAgent(BaseAgent):
    """Backend Development Agent responsible for creating backend/API code."""
    
    def __init__(self):
        super().__init__("Backend Developer", "Backend Development & API Design")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create backend application based on design document."""
        
        self.update_status(self.agent.status, 10, "Analyzing backend requirements")
        
        if not design_doc:
            raise ValueError("Design document is required for backend development")
        
        # Determine backend framework based on language
        if language in ["JavaScript/TypeScript", "JavaScript", "TypeScript"]:
            files = await self._create_node_backend(project_description, design_doc)
        elif language == "Python":
            files = await self._create_python_backend(project_description, design_doc)
        elif language == "Java":
            files = await self._create_java_backend(project_description, design_doc)
        elif language == "C#":
            files = await self._create_csharp_backend(project_description, design_doc)
        elif language == "Go":
            files = await self._create_go_backend(project_description, design_doc)
        else:
            files = await self._create_generic_backend(project_description, design_doc, language)
        
        self.log(LogLevel.SUCCESS, f"Created {len(files)} backend files")
        return files
    
    async def _create_python_backend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create FastAPI backend files."""
        files = []
        
        # Create main.py
        self.update_status(self.agent.status, 20, "Creating FastAPI main application")
        
        main_prompt = f"""
        Create a comprehensive FastAPI main.py application based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create a complete FastAPI application that includes:
        1. FastAPI app initialization with proper configuration
        2. CORS middleware for frontend integration
        3. All required API endpoints based on the design
        4. Proper error handling and validation
        5. Pydantic models for request/response
        6. Authentication if required
        7. File upload handling if needed
        8. WebSocket support for real-time updates
        9. Background tasks if applicable
        10. Health check endpoint
        
        Follow FastAPI best practices and include proper documentation.
        """
        
        main_content = await self.call_openai([
            {"role": "system", "content": "You are an expert Python FastAPI developer. Write production-ready, well-structured code."},
            {"role": "user", "content": main_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/main.py",
            content=main_content,
            type=FileType.BACKEND
        ))
        
        # Create models.py
        self.update_status(self.agent.status, 35, "Creating Pydantic models")
        
        models_prompt = f"""
        Create comprehensive Pydantic models based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create models.py with:
        1. All data models from the design document
        2. Request/response models for APIs
        3. Proper validation rules
        4. Enum classes where appropriate
        5. Base models for common patterns
        6. Database models if applicable
        7. Type hints and documentation
        
        Export all models properly.
        """
        
        models_content = await self.call_openai([
            {"role": "system", "content": "You are an expert in Python data modeling with Pydantic. Create robust, validated models."},
            {"role": "user", "content": models_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/models.py",
            content=models_content,
            type=FileType.BACKEND
        ))
        
        # Create API routes
        self.update_status(self.agent.status, 50, "Creating API routes")
        
        routes_prompt = f"""
        Create FastAPI router modules based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create api_routes.py with:
        1. APIRouter setup
        2. All endpoints from the design document
        3. Proper HTTP methods and status codes
        4. Request/response validation
        5. Error handling for each endpoint
        6. Documentation strings
        7. Authentication/authorization if needed
        8. File handling endpoints if required
        
        Follow REST API best practices.
        """
        
        routes_content = await self.call_openai([
            {"role": "system", "content": "You are an expert in REST API design with FastAPI. Create well-structured, documented APIs."},
            {"role": "user", "content": routes_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/api_routes.py",
            content=routes_content,
            type=FileType.BACKEND
        ))
        
        # Create business logic services
        self.update_status(self.agent.status, 65, "Creating business logic services")
        
        services_prompt = f"""
        Create business logic services based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create services.py with:
        1. Business logic functions
        2. Data processing utilities
        3. External API integrations
        4. File processing functions
        5. Validation logic
        6. Background task functions
        7. Proper error handling
        8. Async/await patterns where beneficial
        
        Separate business logic from API routes.
        """
        
        services_content = await self.call_openai([
            {"role": "system", "content": "You are an expert in Python backend architecture. Create clean, maintainable business logic."},
            {"role": "user", "content": services_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/services.py",
            content=services_content,
            type=FileType.BACKEND
        ))
        
        # Create configuration
        self.update_status(self.agent.status, 80, "Creating configuration files")
        
        config_content = """
import os
from typing import List
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Engineering Team API"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # File uploads
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    upload_dir: str = "./uploads"
    
    # API Keys
    openai_api_key: str = ""
    
    class Config:
        env_file = ".env"


settings = Settings()
"""
        
        files.append(GeneratedFile(
            path="backend/config.py",
            content=config_content,
            type=FileType.BACKEND
        ))
        
        # Create requirements.txt
        self.update_status(self.agent.status, 90, "Creating requirements file")
        
        requirements_content = """
fastapi>=0.104.1
uvicorn[standard]>=0.24.0
python-multipart>=0.0.6
pydantic>=2.5.0
python-dotenv>=1.0.0
aiofiles>=23.2.1
httpx>=0.25.2
websockets>=12.0
"""
        
        files.append(GeneratedFile(
            path="backend/requirements.txt",
            content=requirements_content,
            type=FileType.BACKEND
        ))
        
        # Create startup script
        startup_content = """
#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"""
        
        files.append(GeneratedFile(
            path="backend/start.sh",
            content=startup_content,
            type=FileType.BACKEND
        ))
        
        return files
    
    async def _create_node_backend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create Node.js/Express backend files."""
        files = []
        
        # Create package.json
        self.update_status(self.agent.status, 25, "Creating Node.js package configuration")
        
        package_json_content = {
            "name": "engineering-team-backend",
            "version": "1.0.0",
            "description": "Backend API for Engineering Team",
            "main": "server.js",
            "type": "module",
            "scripts": {
                "start": "node server.js",
                "dev": "nodemon server.js",
                "build": "tsc",
                "test": "jest"
            },
            "dependencies": {
                "express": "^4.18.2",
                "cors": "^2.8.5",
                "helmet": "^7.1.0",
                "morgan": "^1.10.0",
                "multer": "^1.4.5-lts.1",
                "express-validator": "^7.0.1",
                "dotenv": "^16.3.1",
                "openai": "^4.20.1",
                "ws": "^8.14.2",
                "compression": "^1.7.4"
            },
            "devDependencies": {
                "nodemon": "^3.0.1",
                "@types/node": "^20.8.0",
                "typescript": "^5.2.2"
            }
        }
        
        files.append(GeneratedFile(
            path="backend/package.json",
            content=json.dumps(package_json_content, indent=2),
            type=FileType.BACKEND
        ))
        
        # Create main server file
        self.update_status(self.agent.status, 50, "Creating Express server")
        
        server_prompt = f"""
        Create a comprehensive Express.js server based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create server.js with:
        1. Express app setup with middleware
        2. CORS configuration for frontend
        3. All API routes from design document
        4. Error handling middleware
        5. File upload handling
        6. WebSocket support for real-time updates
        7. Security middleware (helmet, etc.)
        8. Logging with morgan
        9. Environment configuration
        10. Graceful shutdown handling
        
        Use modern ES6+ syntax and best practices.
        """
        
        server_content = await self.call_openai([
            {"role": "system", "content": "You are an expert Node.js/Express developer. Write production-ready, secure code."},
            {"role": "user", "content": server_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/server.js",
            content=server_content,
            type=FileType.BACKEND
        ))
        
        return files
    
    async def _create_java_backend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create Spring Boot backend files."""
        files = []
        
        self.update_status(self.agent.status, 30, "Creating Spring Boot application")
        
        # Create main application class
        spring_prompt = f"""
        Create a Spring Boot application based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create Application.java with:
        1. Spring Boot main class
        2. REST controllers for all endpoints
        3. Service layer for business logic
        4. Data models/entities
        5. Configuration classes
        6. CORS configuration
        7. Exception handling
        8. File upload handling
        
        Follow Spring Boot best practices.
        """
        
        spring_content = await self.call_openai([
            {"role": "system", "content": "You are an expert Spring Boot developer. Write clean, well-structured Java code."},
            {"role": "user", "content": spring_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/src/main/java/com/engineeringteam/Application.java",
            content=spring_content,
            type=FileType.BACKEND
        ))
        
        return files
    
    async def _create_csharp_backend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create ASP.NET Core backend files."""
        files = []
        
        self.update_status(self.agent.status, 30, "Creating ASP.NET Core application")
        
        dotnet_prompt = f"""
        Create an ASP.NET Core Web API based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create Program.cs and controllers following .NET 6+ patterns.
        Include all required endpoints, models, and services.
        """
        
        dotnet_content = await self.call_openai([
            {"role": "system", "content": "You are an expert ASP.NET Core developer. Write modern C# code."},
            {"role": "user", "content": dotnet_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/Program.cs",
            content=dotnet_content,
            type=FileType.BACKEND
        ))
        
        return files
    
    async def _create_go_backend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create Go backend files."""
        files = []
        
        self.update_status(self.agent.status, 30, "Creating Go web server")
        
        go_prompt = f"""
        Create a Go web server using Gin or standard library based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create main.go with all required handlers and middleware.
        """
        
        go_content = await self.call_openai([
            {"role": "system", "content": "You are an expert Go developer. Write idiomatic Go code."},
            {"role": "user", "content": go_prompt}
        ])
        
        files.append(GeneratedFile(
            path="backend/main.go",
            content=go_content,
            type=FileType.BACKEND
        ))
        
        return files
    
    async def _create_generic_backend(self, project_description: str, design_doc: str, language: str) -> List[GeneratedFile]:
        """Create generic backend for other languages."""
        files = []
        
        self.update_status(self.agent.status, 50, f"Creating {language} backend")
        
        generic_prompt = f"""
        Create backend application files for {language} based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create appropriate backend files following {language} best practices.
        """
        
        content = await self.call_openai([
            {"role": "system", "content": f"You are an expert {language} developer."},
            {"role": "user", "content": generic_prompt}
        ])
        
        files.append(GeneratedFile(
            path=f"backend/main.{language.lower().replace('/', '_')}",
            content=content,
            type=FileType.BACKEND
        ))
        
        return files
