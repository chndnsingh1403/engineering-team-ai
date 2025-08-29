import asyncio
import uuid
import os
import zipfile
import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Callable
from agents.lead_agent import LeadAgent
from agents.frontend_dev_agent import FrontendDevAgent
from agents.backend_dev_agent import BackendDevAgent
from agents.test_dev_agent import TestDevAgent
from agents.documentation_agent import DocumentationAgent
from models import (
    Project, ProjectStatus, Agent, LogEntry, LogLevel, 
    GeneratedFile, ProcessingStatus, AgentStatus
)
from config import settings


class EngineeringTeamOrchestrator:
    """Orchestrates the engineering team agents to complete project requests."""
    
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.active_projects: Dict[str, asyncio.Task] = {}
        
        # Initialize agents
        self.lead_agent = LeadAgent()
        self.frontend_agent = FrontendDevAgent()
        self.backend_agent = BackendDevAgent()
        self.test_agent = TestDevAgent()
        self.documentation_agent = DocumentationAgent()
        
        self.agents = [
            self.lead_agent,
            self.frontend_agent,
            self.backend_agent,
            self.test_agent,
            self.documentation_agent
        ]
        
        # WebSocket connections for real-time updates
        self.websocket_connections: Dict[str, List[Any]] = {}
    
    def _generate_project_folder_name(self, project_id: str, description: str) -> str:
        """Generate a descriptive folder name from project description and ID."""
        # Clean the description to make it filesystem-friendly
        clean_desc = re.sub(r'[^\w\s-]', '', description.lower())
        clean_desc = re.sub(r'\s+', '-', clean_desc.strip())
        
        # Limit description length
        max_desc_length = 40
        if len(clean_desc) > max_desc_length:
            clean_desc = clean_desc[:max_desc_length].rstrip('-')
        
        # Get short version of project ID (first 8 characters)
        short_id = project_id[:8]
        
        # Combine description with short ID
        folder_name = f"{clean_desc}_{short_id}"
        
        return folder_name
    
    def add_websocket_connection(self, project_id: str, websocket):
        """Add a WebSocket connection for project updates."""
        if project_id not in self.websocket_connections:
            self.websocket_connections[project_id] = []
        self.websocket_connections[project_id].append(websocket)
    
    def remove_websocket_connection(self, project_id: str, websocket):
        """Remove a WebSocket connection."""
        if project_id in self.websocket_connections:
            if websocket in self.websocket_connections[project_id]:
                self.websocket_connections[project_id].remove(websocket)
    
    async def broadcast_update(self, project_id: str, update_data: Dict[str, Any]):
        """Broadcast update to all connected WebSocket clients."""
        if project_id in self.websocket_connections:
            disconnected = []
            for ws in self.websocket_connections[project_id]:
                try:
                    await ws.send_json(update_data)
                except Exception:
                    disconnected.append(ws)
            
            # Remove disconnected WebSockets
            for ws in disconnected:
                self.websocket_connections[project_id].remove(ws)
    
    def create_project(self, description: str, language: str) -> Project:
        """Create a new project."""
        project_id = str(uuid.uuid4())
        project = Project(
            id=project_id,
            description=description,
            language=language,
            status=ProjectStatus.PENDING,
            created_at=datetime.now()
        )
        
        # Initialize agents for this project
        for agent in self.agents:
            project.agents.append(Agent(
                id=agent.agent.id,
                name=agent.agent.name,
                role=agent.agent.role,
                status=AgentStatus.IDLE
            ))
        
        self.projects[project_id] = project
        return project
    
    def log_message(self, project_id: str, level: LogLevel, agent: str, message: str):
        """Add a log entry for a project."""
        if project_id in self.projects:
            log_entry = LogEntry(
                id=str(uuid.uuid4()),
                timestamp=datetime.now(),
                agent=agent,
                level=level,
                message=message
            )
            self.projects[project_id].logs.append(log_entry)
            
            # Broadcast log update
            asyncio.create_task(self.broadcast_update(project_id, {
                "type": "log_update",
                "log": log_entry.dict()
            }))
    
    def update_agent_status(self, project_id: str, agent_id: str, status: AgentStatus, progress: int = None, current_task: str = None):
        """Update agent status for a project."""
        if project_id in self.projects:
            for agent in self.projects[project_id].agents:
                if agent.id == agent_id:
                    agent.status = status
                    if progress is not None:
                        agent.progress = progress
                    if current_task is not None:
                        agent.current_task = current_task
                    break
            
            # Broadcast agent update
            asyncio.create_task(self.broadcast_update(project_id, {
                "type": "agent_update",
                "agents": [agent.dict() for agent in self.projects[project_id].agents]
            }))
    
    async def process_project(self, project_id: str) -> Project:
        """Process a project through all engineering agents with detailed progress tracking."""
        print(f"🔄 Processing project {project_id}")
        
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        project.status = ProjectStatus.PROCESSING
        print(f"📊 Project status set to PROCESSING for {project_id}")
        
        try:
            self.log_message(project_id, LogLevel.INFO, "System", "Starting project processing")
            print(f"📝 Log message sent for project {project_id}")
            
            # Set up agent callbacks
            for agent in self.agents:
                agent.set_callbacks(
                    log_callback=lambda log_entry, pid=project_id: self.log_message(
                        pid, log_entry.level, log_entry.agent, log_entry.message
                    ),
                    status_callback=lambda agent_status, pid=project_id: self.update_agent_status(
                        pid, agent_status.id, agent_status.status, 
                        agent_status.progress, agent_status.current_task
                    )
                )
            
            # Phase 1: Lead Agent - Create design document
            self.log_message(project_id, LogLevel.INFO, "System", "Phase 1: Creating system design")
            design_files = await self.lead_agent.run(
                project.description, 
                project.language
            )
            project.files.extend(design_files)
            
            # Extract design document content
            design_doc = ""
            for file in design_files:
                if "SYSTEM_DESIGN" in file.path or "design" in file.path.lower():
                    design_doc += f"\n{file.content}\n"
            
            # Phase 2: Frontend Agent - Create frontend code
            self.log_message(project_id, LogLevel.INFO, "System", "Phase 2: Developing frontend")
            frontend_files = await self.frontend_agent.run(
                project.description,
                project.language,
                design_doc
            )
            project.files.extend(frontend_files)
            
            # Phase 3: Backend Agent - Create backend code
            self.log_message(project_id, LogLevel.INFO, "System", "Phase 3: Developing backend")
            backend_files = await self.backend_agent.run(
                project.description,
                project.language,
                design_doc
            )
            project.files.extend(backend_files)
            
            # Phase 4: Test Agent - Create tests
            self.log_message(project_id, LogLevel.INFO, "System", "Phase 4: Creating test suites")
            test_files = await self.test_agent.run(
                project.description,
                project.language,
                design_doc,
                {
                    "generated_files": [
                        {"path": f.path, "content": f.content, "type": f.type.value}
                        for f in project.files
                    ]
                }
            )
            project.files.extend(test_files)
            
            # Phase 5: Documentation Agent - Create documentation
            self.log_message(project_id, LogLevel.INFO, "System", "Phase 5: Creating documentation")
            doc_files = await self.documentation_agent.run(
                project.description,
                project.language,
                design_doc,
                {
                    "generated_files": [
                        {"path": f.path, "content": f.content, "type": f.type.value}
                        for f in project.files
                    ]
                }
            )
            project.files.extend(doc_files)
            
            # Create project ZIP file
            zip_path = await self.create_project_zip(project_id)
            self.log_message(project_id, LogLevel.SUCCESS, "System", f"Project ZIP created: {zip_path}")
            
            project.status = ProjectStatus.COMPLETED
            project.completed_at = datetime.now()
            
            self.log_message(project_id, LogLevel.SUCCESS, "System", "Project completed successfully!")
            
            # Broadcast completion
            await self.broadcast_update(project_id, {
                "type": "project_completed",
                "project": project.dict()
            })
            
        except Exception as e:
            project.status = ProjectStatus.FAILED
            self.log_message(project_id, LogLevel.ERROR, "System", f"Project failed: {str(e)}")
            
            # Broadcast failure
            await self.broadcast_update(project_id, {
                "type": "project_failed",
                "error": str(e)
            })
            
            raise
        
        return project
    
    async def start_project(self, project_id: str) -> asyncio.Task:
        """Start processing a project asynchronously."""
        print(f"🚀 Starting project processing for {project_id}")
        
        if project_id in self.active_projects:
            raise ValueError(f"Project {project_id} is already being processed")
        
        task = asyncio.create_task(self.process_project(project_id))
        self.active_projects[project_id] = task
        
        # Clean up task when done
        def cleanup(task):
            if project_id in self.active_projects:
                del self.active_projects[project_id]
        
        task.add_done_callback(cleanup)
        return task
    
    async def create_project_zip(self, project_id: str) -> str:
        """Create a ZIP file containing all generated files."""
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        # Generate descriptive folder name
        folder_name = self._generate_project_folder_name(project_id, project.description)
        output_dir = os.path.join(settings.output_dir, folder_name)
        os.makedirs(output_dir, exist_ok=True)
        
        # Write all files to disk
        for file in project.files:
            file_path = os.path.join(output_dir, file.path)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(file.content)
        
        # Create ZIP file
        zip_path = os.path.join(output_dir, f"{folder_name}-project.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in project.files:
                file_path = os.path.join(output_dir, file.path)
                if os.path.exists(file_path):
                    zipf.write(file_path, file.path)
        
        return zip_path
    
    def get_project(self, project_id: str) -> Optional[Project]:
        """Get a project by ID."""
        return self.projects.get(project_id)
    
    def get_project_status(self, project_id: str) -> Optional[ProcessingStatus]:
        """Get current processing status of a project."""
        if project_id not in self.projects:
            return None
        
        project = self.projects[project_id]
        
        # Calculate overall progress
        total_progress = sum(agent.progress for agent in project.agents)
        overall_progress = round(total_progress / len(project.agents)) if project.agents else 0
        
        # Determine current phase
        current_phase = "Initializing"
        if project.status == ProjectStatus.PROCESSING:
            working_agents = [a for a in project.agents if a.status == AgentStatus.WORKING]
            if working_agents:
                current_phase = f"Working: {working_agents[0].role}"
            else:
                completed_agents = [a for a in project.agents if a.status == AgentStatus.COMPLETED]
                if len(completed_agents) == len(project.agents):
                    current_phase = "Finalizing"
                else:
                    current_phase = f"Phase {len(completed_agents) + 1}"
        elif project.status == ProjectStatus.COMPLETED:
            current_phase = "Completed"
        elif project.status == ProjectStatus.FAILED:
            current_phase = "Failed"
        
        return ProcessingStatus(
            request_id=project_id,
            agents=project.agents,
            overall_progress=overall_progress,
            current_phase=current_phase,
            logs=project.logs[-50:]  # Return last 50 logs
        )
    
    def get_all_projects(self) -> List[Project]:
        """Get all projects."""
        return list(self.projects.values())
