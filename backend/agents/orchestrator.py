import asyncio
import uuid
import os
import shutil
import zipfile
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional
from pathlib import Path

from .lead_agent import LeadAgent
from .frontend_dev_agent import FrontendDevAgent
from .backend_dev_agent import BackendDevAgent
from .test_dev_agent import TestDevAgent
from .documentation_agent import DocumentationAgent
from models import (
    Project, ProjectStatus, Agent, LogEntry, LogLevel, 
    GeneratedFile, ProcessingStatus, AgentStatus
)
from config import settings


class AgentOrchestrator:
    """Orchestrates the execution of multiple AI agents for project development."""
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.active_processes: Dict[str, asyncio.Task] = {}
        self.status_callbacks: Dict[str, List[Callable]] = {}
        
    def add_status_callback(self, project_id: str, callback: Callable[[ProcessingStatus], None]):
        """Add a callback for status updates."""
        if project_id not in self.status_callbacks:
            self.status_callbacks[project_id] = []
        self.status_callbacks[project_id].append(callback)
    
    def remove_status_callback(self, project_id: str, callback: Callable):
        """Remove a status update callback."""
        if project_id in self.status_callbacks and callback in self.status_callbacks[project_id]:
            self.status_callbacks[project_id].remove(callback)
    
    def _notify_status_update(self, project_id: str, status: ProcessingStatus):
        """Notify all registered callbacks of a status update."""
        if project_id in self.status_callbacks:
            for callback in self.status_callbacks[project_id]:
                try:
                    callback(status)
                except Exception as e:
                    print(f"Error in status callback: {e}")
    
    def _create_log_callback(self, project_id: str):
        """Create a log callback function for agents."""
        def log_callback(log_entry: LogEntry):
            if project_id in self.projects:
                self.projects[project_id].logs.append(log_entry)
                self._update_status(project_id)
        return log_callback
    
    def _create_agent_status_callback(self, project_id: str):
        """Create an agent status callback function."""
        def status_callback(agent: Agent):
            if project_id in self.projects:
                project = self.projects[project_id]
                # Update the specific agent in the project
                for i, existing_agent in enumerate(project.agents):
                    if existing_agent.id == agent.id:
                        project.agents[i] = agent
                        break
                self._update_status(project_id)
        return status_callback
    
    def _update_status(self, project_id: str):
        """Update and broadcast project status."""
        if project_id not in self.projects:
            return
            
        project = self.projects[project_id]
        
        # Calculate overall progress
        if project.agents:
            total_progress = sum(agent.progress for agent in project.agents)
            overall_progress = total_progress // len(project.agents)
        else:
            overall_progress = 0
        
        # Determine current phase
        current_phase = "Initializing"
        for agent in project.agents:
            if agent.status == AgentStatus.WORKING:
                current_phase = f"{agent.name}: {agent.current_task or 'Working'}"
                break
        
        if all(agent.status == AgentStatus.COMPLETED for agent in project.agents):
            current_phase = "Completed"
            overall_progress = 100
            project.status = ProjectStatus.COMPLETED
            project.completed_at = datetime.now()
        elif any(agent.status == AgentStatus.FAILED for agent in project.agents):
            current_phase = "Failed"
            project.status = ProjectStatus.FAILED
        
        status = ProcessingStatus(
            request_id=project_id,
            agents=project.agents,
            overall_progress=overall_progress,
            current_phase=current_phase,
            logs=project.logs[-50:]  # Keep only last 50 logs
        )
        
        self._notify_status_update(project_id, status)
    
    async def create_project(self, description: str, language: str, files: Optional[List[str]] = None) -> str:
        """Create a new project and return its ID."""
        project_id = str(uuid.uuid4())
        
        project = Project(
            id=project_id,
            description=description,
            language=language,
            status=ProjectStatus.PENDING,
            created_at=datetime.now(),
            files=[],
            agents=[],
            logs=[]
        )
        
        if files:
            project.files = files
        
        self.projects[project_id] = project
        return project_id
    
    async def start_processing(self, project_id: str):
        """Start processing a project with all agents."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        if project_id in self.active_processes:
            raise ValueError(f"Project {project_id} is already being processed")
        
        # Start the processing task
        task = asyncio.create_task(self._process_project(project_id))
        self.active_processes[project_id] = task
        
        try:
            await task
        finally:
            # Clean up the active process
            if project_id in self.active_processes:
                del self.active_processes[project_id]
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.projects.get(project_id)


# Global orchestrator instance
orchestrator = AgentOrchestrator()