from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel


class AgentStatus(str, Enum):
    IDLE = "idle"
    WORKING = "working" 
    COMPLETED = "completed"
    FAILED = "failed"


class ProjectStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class FileType(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    TEST = "test"
    DOCUMENTATION = "documentation"
    DESIGN = "design"


class LogLevel(str, Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class ProjectRequest(BaseModel):
    description: str
    language: str
    files: Optional[List[str]] = None


class Agent(BaseModel):
    id: str
    name: str
    role: str
    status: AgentStatus = AgentStatus.IDLE
    progress: int = 0
    current_task: Optional[str] = None
    output: Optional[str] = None


class LogEntry(BaseModel):
    id: str
    timestamp: datetime
    agent: str
    level: LogLevel
    message: str


class GeneratedFile(BaseModel):
    path: str
    content: str
    type: FileType


class ProcessingStatus(BaseModel):
    request_id: str
    agents: List[Agent]
    overall_progress: int
    current_phase: str
    logs: List[LogEntry]


class ProjectOutput(BaseModel):
    request_id: str
    files: List[GeneratedFile]
    download_url: Optional[str] = None
    summary: str


class Project(BaseModel):
    id: str
    description: str
    language: str
    status: ProjectStatus = ProjectStatus.PENDING
    created_at: datetime
    completed_at: Optional[datetime] = None
    files: List[GeneratedFile] = []
    agents: List[Agent] = []
    logs: List[LogEntry] = []
