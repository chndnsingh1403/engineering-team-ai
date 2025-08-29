import asyncio
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from openai import AsyncOpenAI
from models import Agent, AgentStatus, LogEntry, LogLevel, GeneratedFile
from config import settings


class BaseAgent(ABC):
    """Base class for all AI agents in the engineering team."""
    
    def __init__(self, name: str, role: str):
        self.agent = Agent(
            id=str(uuid.uuid4()),
            name=name,
            role=role,
            status=AgentStatus.IDLE
        )
        # Initialize LLM client based on provider
        self.client = self._initialize_llm_client()
        self.log_callback: Optional[Callable[[LogEntry], None]] = None
        self.status_callback: Optional[Callable[[Agent], None]] = None
    
    def _initialize_llm_client(self):
        """Initialize the appropriate LLM client based on configuration."""
        provider = settings.llm_provider.lower()
        
        if provider == "openai":
            return AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url
            )
        elif provider == "gemini":
            # For Gemini using OpenAI-compatible API
            return AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url
            )
        elif provider == "anthropic":
            # For Anthropic using OpenAI-compatible API (via OpenRouter)
            return AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url=settings.llm_base_url
            )
        elif provider == "ollama":
            # For local Ollama using OpenAI-compatible API
            return AsyncOpenAI(
                api_key=settings.llm_api_key or "ollama",
                base_url=settings.llm_base_url
            )
        else:
            # Default to OpenAI
            return AsyncOpenAI(
                api_key=settings.llm_api_key,
                base_url="https://api.openai.com/v1"
            )
    
    def set_callbacks(self, log_callback: Callable[[LogEntry], None], status_callback: Callable[[Agent], None]):
        """Set callbacks for logging and status updates."""
        self.log_callback = log_callback
        self.status_callback = status_callback
    
    def update_progress(self, progress: int, current_task: str):
        """Update agent progress and current task."""
        self.agent.progress = progress
        self.agent.current_task = current_task
        if self.status_callback:
            self.status_callback(self.agent)
    
    def log(self, level: LogLevel, message: str):
        """Log a message."""
        if self.log_callback:
            log_entry = LogEntry(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                agent=self.agent.name,
                level=level,
                message=message
            )
            self.log_callback(log_entry)
    
    def update_status(self, status: AgentStatus, progress: int = None, current_task: str = None):
        """Update agent status."""
        self.agent.status = status
        if progress is not None:
            self.agent.progress = progress
        if current_task is not None:
            self.agent.current_task = current_task
        
        if self.status_callback:
            self.status_callback(self.agent)
    
    async def _call_llm(self, messages: List[Dict[str, str]], system_prompt: str = None) -> str:
        """Make an LLM API call with fallback to mock mode."""
        
        # Check if we're in mock mode or should fallback to mock
        if settings.mock_mode:
            return await self._mock_llm_response(messages, system_prompt)
        
        try:
            # Prepare messages
            if system_prompt:
                full_messages = [{"role": "system", "content": system_prompt}] + messages
            else:
                full_messages = messages
            
            # Make the API call
            response = await self.client.chat.completions.create(
                model=settings.llm_model,
                messages=full_messages,
                temperature=0.7,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.log(f"LLM API call failed: {e}", LogLevel.ERROR)
            
            # Fallback to mock mode if API fails
            if "429" in str(e) or "quota" in str(e).lower():
                self.log("Falling back to mock mode due to quota limits", LogLevel.WARNING)
                return await self._mock_llm_response(messages, system_prompt)
            else:
                raise e
    
    async def _mock_llm_response(self, messages: List[Dict[str, str]], system_prompt: str = None) -> str:
        """Generate a mock response for demo purposes."""
        
        # Simulate processing time
        await asyncio.sleep(2)
        
        # Generate context-appropriate mock response based on agent type
        if "Frontend" in self.agent.role:
            return """# Frontend Implementation Plan

## Components Structure
```
src/
  components/
    TodoItem.tsx
    TodoList.tsx
    AddTodoForm.tsx
  pages/
    TodoApp.tsx
  styles/
    main.css
```

## Key Features
- Responsive design with modern UI
- Add/edit/delete todo functionality
- Mark items as complete
- Filter by status (all/active/completed)
- Local storage persistence

## Technology Stack
- React 18 with TypeScript
- CSS Modules for styling
- React Hooks for state management
"""
            
        elif "Backend" in self.agent.role:
            return """# Backend API Design

## API Endpoints
- GET /api/todos - List all todos
- POST /api/todos - Create new todo
- PUT /api/todos/:id - Update todo
- DELETE /api/todos/:id - Delete todo

## Data Model
```typescript
interface Todo {
  id: string;
  title: string;
  completed: boolean;
  createdAt: Date;
  updatedAt: Date;
}
```

## Implementation
- Express.js with TypeScript
- In-memory storage (for demo)
- Input validation with Joi
- CORS enabled for frontend
"""
            
        elif "Test" in self.agent.role:
            return """# Testing Strategy

## Unit Tests
- Component testing with Jest & React Testing Library
- API endpoint testing with Supertest
- Utility function tests

## Integration Tests
- Full user flow testing
- API integration tests
- Cross-browser compatibility

## Test Files
- TodoApp.test.tsx
- api.test.ts
- utils.test.ts

## Coverage Goals
- 90%+ code coverage
- All critical paths tested
"""
            
        elif "Documentation" in self.agent.role or "Technical Writer" in self.agent.role:
            return """# Project Documentation

## README.md
# Todo App
A simple, elegant todo application built with React and Node.js.

## Features
- ✅ Add new todos
- ✅ Mark todos as complete
- ✅ Delete todos
- ✅ Filter by status
- ✅ Responsive design

## Getting Started
1. Clone the repository
2. Install dependencies: `npm install`
3. Start development server: `npm run dev`
4. Open http://localhost:3000

## API Documentation
Full API documentation available in `/docs/api.md`

## Contributing
Please read CONTRIBUTING.md for guidelines.
"""
            
        else:  # Lead Agent
            return """# System Design Document

## Project Overview
Simple Todo Application with modern web technologies.

## Architecture
- **Frontend**: React 18 + TypeScript + Vite
- **Backend**: Node.js + Express + TypeScript  
- **Storage**: In-memory (demo) / JSON file persistence
- **Styling**: CSS Modules with responsive design

## Component Breakdown
1. **Frontend Components**
   - TodoApp (main container)
   - TodoList (list display)
   - TodoItem (individual item)
   - AddTodoForm (input form)

2. **Backend Services**
   - Todo CRUD API
   - Validation middleware
   - Error handling

3. **Testing**
   - Unit tests for all components
   - API integration tests
   - E2E testing setup

## Development Phases
1. System Design ✅
2. Frontend Development
3. Backend Development  
4. Testing Implementation
5. Documentation
"""
    
    @abstractmethod
    async def execute(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Execute the agent's task and return generated files."""
        pass
    
    async def run(
        self,
        project_description: str,
        language: str,
        design_doc: Optional[str] = None,
        previous_outputs: Optional[Dict[str, Any]] = None
    ) -> List[GeneratedFile]:
        """Run the agent with error handling."""
        try:
            self.update_status(AgentStatus.WORKING, 0, "Starting...")
            self.log(LogLevel.INFO, f"Starting {self.agent.role}")
            
            result = await self.execute(project_description, language, design_doc, previous_outputs)
            
            self.update_status(AgentStatus.COMPLETED, 100, "Completed")
            self.log(LogLevel.SUCCESS, f"Completed {self.agent.role}")
            
            return result
        except Exception as e:
            self.update_status(AgentStatus.FAILED, self.agent.progress, f"Failed: {str(e)}")
            self.log(LogLevel.ERROR, f"Agent failed: {str(e)}")
            raise
