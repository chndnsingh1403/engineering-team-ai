import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from models import GeneratedFile, FileType, LogLevel, AgentStatus


class LeadAgent(BaseAgent):
    """Lead Agent responsible for creating the design document and project flow."""
    
    def __init__(self):
        super().__init__("Lead Architect", "Project Lead & System Design")
    
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Create system design and architecture for the project."""
        self.log(LogLevel.INFO, "🎯 Lead Agent starting system design analysis")
        
        self.update_status(AgentStatus.WORKING, 10, "Analyzing project requirements")
        await asyncio.sleep(1)  # Simulate processing time
        
        self.log(LogLevel.INFO, "📊 Breaking down project requirements and identifying key components")
        self.update_progress(25, "Creating system architecture")
        await asyncio.sleep(1)
        
        # Create design document
        design_prompt = f"""
        As a Lead Software Architect, analyze the following project requirements and create a comprehensive design document.
        
        Project Description: {project_description}
        Primary Language: {language}
        
        Create a detailed design document that includes:
        
        1. PROJECT OVERVIEW
        - Executive summary
        - Key objectives and goals
        - Target audience/users
        
        2. SYSTEM ARCHITECTURE
        - High-level architecture diagram (text description)
        - Component breakdown
        - Technology stack recommendations
        - Database design (if applicable)
        
        3. FRONTEND REQUIREMENTS
        - User interface design principles
        - Component structure
        - State management approach
        - Key features and user flows
        
        4. BACKEND REQUIREMENTS
        - API design and endpoints
        - Data models and schemas
        - Business logic components
        - Authentication and security considerations
        
        5. TESTING STRATEGY
        - Unit testing approach
        - Integration testing plan
        - Test coverage goals
        
        6. DOCUMENTATION REQUIREMENTS
        - README structure
        - API documentation needs
        - User guide requirements
        
        7. IMPLEMENTATION PHASES
        - Development phases and milestones
        - Dependencies between components
        - Estimated complexity for each phase
        
        Provide detailed, actionable specifications that other agents can follow to implement the solution.
        """
        
        self.log(LogLevel.INFO, "🏗️ Generating comprehensive system design document")
        self.update_status(AgentStatus.WORKING, 50, "Creating system design")
        await asyncio.sleep(2)  # Simulate AI processing time
        
        design_content = await self._call_llm([
            {"role": "user", "content": design_prompt}
        ], system_prompt="You are an expert software architect with years of experience in system design and project planning.")
        
        self.log(LogLevel.INFO, "📋 Creating detailed implementation roadmap for development team")
        self.update_status(AgentStatus.WORKING, 70, "Creating implementation roadmap")
        await asyncio.sleep(1)
        
        # Create implementation roadmap
        roadmap_prompt = f"""
        Based on the design document created above, create a detailed implementation roadmap.
        
        Design Document:
        {design_content}
        
        Create an IMPLEMENTATION_ROADMAP.md that includes:
        
        1. DEVELOPMENT PHASES
        - Phase 1: Foundation and setup
        - Phase 2: Core backend development
        - Phase 3: Frontend development
        - Phase 4: Integration and testing
        - Phase 5: Documentation and deployment
        
        2. TASK BREAKDOWN
        - Specific tasks for each agent
        - Dependencies between tasks
        - Estimated effort for each task
        
        3. FILE STRUCTURE
        - Complete project directory structure
        - Key files to be created by each agent
        
        4. INTEGRATION POINTS
        - How frontend and backend will communicate
        - Data flow between components
        - Error handling strategies
        
        Make this actionable for the development agents.
        """
        
        roadmap_content = await self._call_llm([
            {"role": "user", "content": roadmap_prompt}
        ], system_prompt="You are an expert project manager specializing in software development workflows.")
        
        files = [
            GeneratedFile(
                path="SYSTEM_DESIGN.md",
                content=design_content,
                type=FileType.DESIGN
            ),
            GeneratedFile(
                path="IMPLEMENTATION_ROADMAP.md", 
                content=roadmap_content,
                type=FileType.DESIGN
            )
        ]
        
        self.log(LogLevel.SUCCESS, f"Created {len(files)} design documents")
        return files
