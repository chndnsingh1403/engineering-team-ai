import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel, AgentStatus


class FrontendDevAgent(BaseAgent):
    """Frontend Developer Agent responsible for creating the frontend application."""
    
    def __init__(self):
        super().__init__("Frontend Developer", "UI/UX Implementation & Frontend Development")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create frontend application based on design document."""
        
        self.log(LogLevel.INFO, "🎨 Frontend Developer starting UI implementation")
        self.update_status(AgentStatus.WORKING, 10, "Analyzing frontend requirements")
        await asyncio.sleep(1)
        
        self.log(LogLevel.INFO, "📱 Designing responsive component architecture")
        self.update_progress(25, "Creating component structure")
        await asyncio.sleep(1)
        
        # Extract frontend requirements from design document
        frontend_prompt = f"""
        As a Senior Frontend Developer, analyze the design document and create a complete frontend application.
        
        Project Description: {project_description}
        Primary Language: {language}
        Design Document: {design_doc if design_doc else "Not provided - create based on project description"}
        
        Create a modern, responsive frontend application with:
        
        1. COMPONENT STRUCTURE
        - Main App component
        - Page components
        - Reusable UI components
        - Utility components
        
        2. STYLING
        - Modern CSS framework (Tailwind CSS preferred)
        - Responsive design
        - Clean, professional interface
        
        3. STATE MANAGEMENT
        - Appropriate state management solution
        - API integration layer
        - Error handling
        
        4. ROUTING
        - Client-side routing setup
        - Protected routes (if needed)
        - Navigation structure
        
        Please create the following files with complete, working code:
        - Main component files
        - Styling files
        - Configuration files
        - Package.json with dependencies
        
        Ensure the code is production-ready, well-commented, and follows best practices.
        """
        
        self.log(LogLevel.INFO, "⚛️ Generating React components and project structure")
        self.update_status(AgentStatus.WORKING, 40, "Creating main components")
        await asyncio.sleep(2)
        
        frontend_code = await self.call_openai([
            {"role": "system", "content": "You are a senior frontend developer expert in React, TypeScript, and modern web development."},
            {"role": "user", "content": frontend_prompt}
        ])
        
        self.log(LogLevel.INFO, "🎨 Building reusable UI components")
        self.update_status(AgentStatus.WORKING, 60, "Creating component structure")
        await asyncio.sleep(1)
        
        # Generate specific components
        components_prompt = f"""
        Based on the project requirements and the initial frontend structure created, generate specific React components.
        
        Project: {project_description}
        Language: {language}
        
        Create these specific components with full implementation:
        
        1. App.tsx - Main application component
        2. MainPage.tsx - Primary page component
        3. Header.tsx - Navigation header
        4. Footer.tsx - Footer component
        5. LoadingSpinner.tsx - Loading indicator
        6. ErrorBoundary.tsx - Error handling
        7. ApiService.ts - API communication layer
        8. types.ts - TypeScript type definitions
        
        Ensure each component is:
        - Fully functional
        - Well-typed (if using TypeScript)
        - Properly styled
        - Includes error handling
        - Has proper props and state management
        """
        
        components_code = await self.call_openai([
            {"role": "system", "content": "You are an expert React developer creating production-ready components."},
            {"role": "user", "content": components_prompt}
        ])
        
        self.update_status(AgentStatus.WORKING, 90, "Creating configuration files")
        
        # Generate configuration and setup files
        config_prompt = f"""
        Create the necessary configuration files for a {language} frontend project:
        
        1. package.json - with all necessary dependencies
        2. tsconfig.json - TypeScript configuration
        3. tailwind.config.js - Tailwind CSS configuration
        4. vite.config.ts - Vite configuration
        5. index.html - Main HTML file
        6. index.css - Global styles
        7. .env.example - Environment variables example
        8. README.md - Setup and development instructions
        
        Ensure all configurations are optimized for development and production.
        """
        
        config_files = await self.call_openai([
            {"role": "system", "content": "You are a frontend build engineer expert in project configuration and tooling."},
            {"role": "user", "content": config_prompt}
        ])
        
        # Parse and create individual files from the responses
        files = []
        
        # Add main implementation files
        files.extend([
            GeneratedFile(
                path="frontend/src/App.tsx",
                content=self._extract_component_code(frontend_code, "App"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/pages/MainPage.tsx", 
                content=self._extract_component_code(components_code, "MainPage"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/components/Header.tsx",
                content=self._extract_component_code(components_code, "Header"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/components/Footer.tsx",
                content=self._extract_component_code(components_code, "Footer"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/components/LoadingSpinner.tsx",
                content=self._extract_component_code(components_code, "LoadingSpinner"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/components/ErrorBoundary.tsx",
                content=self._extract_component_code(components_code, "ErrorBoundary"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/services/ApiService.ts",
                content=self._extract_component_code(components_code, "ApiService"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/types/index.ts",
                content=self._extract_component_code(components_code, "types"),
                type=FileType.FRONTEND
            )
        ])
        
        # Add configuration files
        files.extend([
            GeneratedFile(
                path="frontend/package.json",
                content=self._extract_config_file(config_files, "package.json"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/tsconfig.json",
                content=self._extract_config_file(config_files, "tsconfig.json"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/tailwind.config.js",
                content=self._extract_config_file(config_files, "tailwind.config.js"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/vite.config.ts",
                content=self._extract_config_file(config_files, "vite.config.ts"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/index.html",
                content=self._extract_config_file(config_files, "index.html"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/src/index.css",
                content=self._extract_config_file(config_files, "index.css"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/.env.example",
                content=self._extract_config_file(config_files, ".env.example"),
                type=FileType.FRONTEND
            ),
            GeneratedFile(
                path="frontend/README.md",
                content=self._extract_config_file(config_files, "README.md"),
                type=FileType.FRONTEND
            )
        ])
        
        self.log(LogLevel.SUCCESS, f"Generated {len(files)} frontend files")
        return files
    
    def _extract_component_code(self, content: str, component_name: str) -> str:
        """Extract specific component code from AI response."""
        # This is a simplified extraction - in a real implementation,
        # you'd want more sophisticated parsing
        lines = content.split('\n')
        in_component = False
        component_lines = []
        
        for line in lines:
            if component_name in line and ('```' in line or 'tsx' in line or 'ts' in line):
                in_component = True
                continue
            if in_component and '```' in line:
                break
            if in_component:
                component_lines.append(line)
        
        if component_lines:
            return '\n'.join(component_lines)
        
        # Fallback: return a basic template
        return f"""// Generated {component_name} component
import React from 'react';

const {component_name}: React.FC = () => {{
  return (
    <div className="p-4">
      <h1>{component_name} Component</h1>
      <p>This component was auto-generated.</p>
    </div>
  );
}};

export default {component_name};
"""
    
    def _extract_config_file(self, content: str, filename: str) -> str:
        """Extract specific configuration file from AI response."""
        # Similar extraction logic for config files
        lines = content.split('\n')
        in_file = False
        file_lines = []
        
        for line in lines:
            if filename in line and ('```' in line or 'json' in line or 'js' in line):
                in_file = True
                continue
            if in_file and '```' in line:
                break
            if in_file:
                file_lines.append(line)
        
        if file_lines:
            return '\n'.join(file_lines)
        
        # Return basic fallback content based on file type
        if filename == 'package.json':
            return """{
  "name": "generated-frontend",
  "version": "1.0.0",
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  }
}"""
        elif filename == 'README.md':
            return f"""# Generated Frontend Application

This frontend application was auto-generated by the Engineering Team AI.

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start development server:
   ```bash
   npm run dev
   ```

## Features

- Modern React application
- TypeScript support
- Responsive design
- Production-ready build setup
"""
        
        return f"# Generated {filename}\n# Configuration file auto-generated by Engineering Team AI"
