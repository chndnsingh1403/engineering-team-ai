import json
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel


class FrontendAgent(BaseAgent):
    """Frontend Development Agent responsible for creating frontend code."""
    
    def __init__(self):
        super().__init__("Frontend Developer", "Frontend Development & UI/UX")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create frontend application based on design document."""
        
        self.update_status(self.agent.status, 10, "Analyzing frontend requirements")
        
        if not design_doc:
            raise ValueError("Design document is required for frontend development")
        
        # Determine frontend framework based on language
        framework_map = {
            "JavaScript/TypeScript": "React with TypeScript",
            "Python": "Streamlit or FastAPI with Jinja2 templates",
            "Java": "Spring Boot with Thymeleaf",
            "C#": "ASP.NET Core MVC",
            "Go": "Go with HTML templates",
            "PHP": "Laravel with Blade templates",
            "Ruby": "Ruby on Rails with ERB",
        }
        
        framework = framework_map.get(language, "React with TypeScript")
        
        # Create package.json or equivalent
        self.update_status(self.agent.status, 20, "Creating project configuration")
        
        if "React" in framework or "JavaScript" in language or "TypeScript" in language:
            files = await self._create_react_frontend(project_description, design_doc)
        elif language == "Python":
            files = await self._create_python_frontend(project_description, design_doc)
        else:
            files = await self._create_generic_frontend(project_description, design_doc, language)
        
        self.log(LogLevel.SUCCESS, f"Created {len(files)} frontend files")
        return files
    
    async def _create_react_frontend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create React frontend files."""
        files = []
        
        # Create package.json
        self.update_status(self.agent.status, 25, "Creating package.json")
        
        package_json_prompt = f"""
        Based on the project requirements and design document, create a modern package.json for a React TypeScript project.
        
        Project: {project_description}
        Design: {design_doc[:1000]}...
        
        Include latest versions of:
        - React 18+
        - TypeScript
        - Vite as build tool
        - Tailwind CSS for styling
        - React Router for navigation
        - Axios for API calls
        - React Hook Form for forms
        - Lucide React for icons
        - Any other relevant dependencies based on the project requirements
        
        Return only valid JSON for package.json.
        """
        
        package_content = await self.call_openai([
            {"role": "system", "content": "You are an expert React developer. Return only valid JSON."},
            {"role": "user", "content": package_json_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/package.json",
            content=package_content,
            type=FileType.FRONTEND
        ))
        
        # Create main App component
        self.update_status(self.agent.status, 40, "Creating main App component")
        
        app_prompt = f"""
        Create a modern React TypeScript App.tsx component based on these requirements:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create a complete, functional App.tsx that includes:
        1. Modern React with TypeScript
        2. Tailwind CSS for styling
        3. React Router setup
        4. Main layout and navigation
        5. Key pages/components structure
        6. Error boundaries
        7. Loading states
        8. Responsive design
        
        Follow modern React best practices and include proper TypeScript types.
        """
        
        app_content = await self.call_openai([
            {"role": "system", "content": "You are an expert React TypeScript developer. Write clean, modern, production-ready code."},
            {"role": "user", "content": app_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/src/App.tsx",
            content=app_content,
            type=FileType.FRONTEND
        ))
        
        # Create main page component
        self.update_status(self.agent.status, 60, "Creating main page components")
        
        main_page_prompt = f"""
        Create a main page component for the React application based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create a comprehensive main page component that includes:
        1. All required functionality from the design
        2. Form handling with validation
        3. API integration setup
        4. Loading and error states
        5. Modern UI with Tailwind CSS
        6. TypeScript interfaces
        7. Accessibility features
        8. Responsive design
        
        Name the file MainPage.tsx and export as default.
        """
        
        main_page_content = await self.call_openai([
            {"role": "system", "content": "You are an expert React developer. Create production-ready, accessible components."},
            {"role": "user", "content": main_page_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/src/pages/MainPage.tsx",
            content=main_page_content,
            type=FileType.FRONTEND
        ))
        
        # Create API service
        self.update_status(self.agent.status, 75, "Creating API service")
        
        api_service_prompt = f"""
        Create an API service file for the React application based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create a complete api.ts service file that includes:
        1. Axios configuration
        2. TypeScript interfaces for API responses
        3. All required API endpoints
        4. Error handling
        5. Request/response interceptors
        6. Authentication handling if needed
        7. Proper TypeScript types
        
        Export all functions and types.
        """
        
        api_content = await self.call_openai([
            {"role": "system", "content": "You are an expert in API integration and TypeScript. Create robust, type-safe API services."},
            {"role": "user", "content": api_service_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/src/services/api.ts",
            content=api_content,
            type=FileType.FRONTEND
        ))
        
        # Create types file
        self.update_status(self.agent.status, 85, "Creating TypeScript types")
        
        types_prompt = f"""
        Create a comprehensive types.ts file for the React application based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Define TypeScript interfaces and types for:
        1. All data models
        2. API request/response types
        3. Component props interfaces
        4. Form data types
        5. State management types
        6. Utility types
        
        Export all types and interfaces.
        """
        
        types_content = await self.call_openai([
            {"role": "system", "content": "You are a TypeScript expert. Create comprehensive, reusable type definitions."},
            {"role": "user", "content": types_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/src/types/index.ts",
            content=types_content,
            type=FileType.FRONTEND
        ))
        
        # Create Tailwind config and CSS
        self.update_status(self.agent.status, 95, "Creating styling configuration")
        
        tailwind_config = """
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
"""
        
        files.append(GeneratedFile(
            path="frontend/tailwind.config.js",
            content=tailwind_config,
            type=FileType.FRONTEND
        ))
        
        css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer components {
  .btn-primary {
    @apply bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors;
  }
  
  .btn-secondary {
    @apply bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-lg transition-colors;
  }
  
  .input-field {
    @apply border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent;
  }
}
"""
        
        files.append(GeneratedFile(
            path="frontend/src/index.css",
            content=css_content,
            type=FileType.FRONTEND
        ))
        
        return files
    
    async def _create_python_frontend(self, project_description: str, design_doc: str) -> List[GeneratedFile]:
        """Create Python frontend (Streamlit) files."""
        files = []
        
        self.update_status(self.agent.status, 30, "Creating Streamlit application")
        
        streamlit_prompt = f"""
        Create a Streamlit application based on these requirements:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create a complete app.py for Streamlit that includes:
        1. All required functionality
        2. Modern UI components
        3. Form handling
        4. File uploads if needed
        5. API integration
        6. Error handling
        7. Session state management
        8. Responsive layout
        
        Use Streamlit's latest features and best practices.
        """
        
        app_content = await self.call_openai([
            {"role": "system", "content": "You are an expert Python developer specializing in Streamlit applications."},
            {"role": "user", "content": streamlit_prompt}
        ])
        
        files.append(GeneratedFile(
            path="frontend/app.py",
            content=app_content,
            type=FileType.FRONTEND
        ))
        
        # Create requirements.txt
        requirements_content = """
streamlit>=1.28.0
requests>=2.31.0
pandas>=2.1.0
plotly>=5.17.0
"""
        
        files.append(GeneratedFile(
            path="frontend/requirements.txt",
            content=requirements_content,
            type=FileType.FRONTEND
        ))
        
        return files
    
    async def _create_generic_frontend(self, project_description: str, design_doc: str, language: str) -> List[GeneratedFile]:
        """Create generic frontend files for other languages."""
        files = []
        
        self.update_status(self.agent.status, 50, f"Creating {language} frontend")
        
        frontend_prompt = f"""
        Create frontend application files for {language} based on:
        
        Project: {project_description}
        Design Document: {design_doc}
        
        Create appropriate frontend files that include:
        1. Main application file
        2. Configuration files
        3. Template files (if applicable)
        4. Static assets setup
        5. API integration
        6. Modern UI/UX practices
        
        Follow {language} best practices and conventions.
        """
        
        content = await self.call_openai([
            {"role": "system", "content": f"You are an expert {language} developer specializing in web frontend development."},
            {"role": "user", "content": frontend_prompt}
        ])
        
        files.append(GeneratedFile(
            path=f"frontend/main.{language.lower().replace('/', '_')}",
            content=content,
            type=FileType.FRONTEND
        ))
        
        return files
