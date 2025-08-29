import os
import aiofiles
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import List, Optional
from pydantic import BaseModel

from config import settings
from models import ProjectRequest, ProjectOutput, ProjectStatus
from orchestrator import EngineeringTeamOrchestrator

# Create FastAPI app
app = FastAPI(
    title="Engineering Team AI",
    description="AI-powered engineering team that designs, codes, tests, and documents projects",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create orchestrator instance
orchestrator = EngineeringTeamOrchestrator()

# Ensure output directory exists
os.makedirs(settings.output_dir, exist_ok=True)
os.makedirs(settings.upload_dir, exist_ok=True)


class SubmitProjectRequest(BaseModel):
    description: str
    language: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Engineering Team AI API",
        "version": "1.0.0",
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}


@app.post("/api/projects/submit")
async def submit_project(
    description: str = Form(...),
    language: str = Form(...),
    files: List[UploadFile] = File(default=[])
):
    """Submit a new project request."""
    try:
        # Validate inputs
        if not description.strip():
            raise HTTPException(status_code=400, detail="Description is required")
        
        if len(description) > 10000:
            raise HTTPException(status_code=400, detail="Description is too long (max 10000 characters)")
        
        # Create project
        project = orchestrator.create_project(description, language)
        
        # Save uploaded files
        if files and files[0].filename:  # Check if files were actually uploaded
            upload_dir = os.path.join(settings.upload_dir, project.id)
            os.makedirs(upload_dir, exist_ok=True)
            
            saved_files = []
            for file in files:
                if file.filename and file.size > 0:
                    # Check file size
                    if file.size > settings.max_file_size:
                        raise HTTPException(
                            status_code=400, 
                            detail=f"File {file.filename} is too large (max {settings.max_file_size} bytes)"
                        )
                    
                    file_path = os.path.join(upload_dir, file.filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        content = await file.read()
                        await f.write(content)
                    saved_files.append(file.filename)
            
            if saved_files:
                orchestrator.log_message(
                    project.id, 
                    "info", 
                    "System", 
                    f"Uploaded files: {', '.join(saved_files)}"
                )
        
        # Start processing asynchronously
        await orchestrator.start_project(project.id)
        
        return {
            "id": project.id,
            "description": project.description,
            "language": project.language,
            "status": project.status.value,
            "created_at": project.created_at.isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/projects/{project_id}/status")
async def get_project_status(project_id: str):
    """Get the processing status of a project."""
    try:
        status = orchestrator.get_project_status(project_id)
        if not status:
            return {
                "error": "Project not found",
                "request_id": project_id,
                "agents": [],
                "overall_progress": 0,
                "current_phase": "Not Found",
                "logs": []
            }
        
        return {
            "request_id": status.request_id,
            "agents": [
                {
                    "id": agent.id,
                    "name": agent.name,
                    "role": agent.role,
                    "status": agent.status,
                    "progress": agent.progress,
                    "current_task": agent.current_task
                }
                for agent in status.agents
            ],
            "overall_progress": status.overall_progress,
            "current_phase": status.current_phase,
            "logs": [
                {
                    "id": log.id,
                    "timestamp": log.timestamp.isoformat(),
                    "agent": log.agent,
                    "level": log.level,
                    "message": log.message
                }
                for log in status.logs
            ]
        }
    except Exception as e:
        print(f"Error in get_project_status: {e}")
        return {
            "error": str(e),
            "request_id": project_id,
            "agents": [],
            "overall_progress": 0,
            "current_phase": "Error",
            "logs": []
        }


@app.get("/api/projects/{project_id}/output")
async def get_project_output(project_id: str):
    """Get the generated files and output of a completed project."""
    project = orchestrator.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status != ProjectStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Project is not completed yet")
    
    # Group files by type for summary
    file_summary = {}
    for file in project.files:
        file_type = file.type.value
        if file_type not in file_summary:
            file_summary[file_type] = 0
        file_summary[file_type] += 1
    
    summary_text = f"Generated {len(project.files)} files: " + ", ".join([
        f"{count} {file_type}" for file_type, count in file_summary.items()
    ])
    
    return {
        "request_id": project_id,
        "files": [
            {
                "path": file.path,
                "content": file.content,
                "type": file.type.value
            }
            for file in project.files
        ],
        "download_url": f"/api/projects/{project_id}/download",
        "summary": summary_text
    }


@app.get("/api/projects/{project_id}/download")
async def download_project(project_id: str):
    """Download the project as a ZIP file."""
    project = orchestrator.get_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project.status != ProjectStatus.COMPLETED:
        raise HTTPException(status_code=400, detail="Project is not completed yet")
    
    try:
        zip_path = await orchestrator.create_project_zip(project_id)
        if not os.path.exists(zip_path):
            raise HTTPException(status_code=404, detail="ZIP file not found")
        
        # Generate descriptive filename
        folder_name = orchestrator._generate_project_folder_name(project_id, project.description)
        
        return FileResponse(
            zip_path,
            media_type='application/zip',
            filename=f"{folder_name}-project.zip"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating ZIP file: {str(e)}")


@app.get("/api/projects")
async def get_all_projects():
    """Get all projects."""
    projects = orchestrator.get_all_projects()
    return [
        {
            "id": project.id,
            "description": project.description[:200] + "..." if len(project.description) > 200 else project.description,
            "language": project.language,
            "status": project.status.value,
            "created_at": project.created_at.isoformat(),
            "completed_at": project.completed_at.isoformat() if project.completed_at else None,
            "file_count": len(project.files)
        }
        for project in projects
    ]


@app.websocket("/ws/{project_id}")
async def websocket_endpoint(websocket: WebSocket, project_id: str):
    """WebSocket endpoint for real-time project updates."""
    await websocket.accept()
    
    # Add connection to orchestrator
    orchestrator.add_websocket_connection(project_id, websocket)
    
    try:
        # Send initial status
        status = orchestrator.get_project_status(project_id)
        if status:
            await websocket.send_json({
                "type": "status_update",
                "data": {
                    "agents": [
                        {
                            "id": agent.id,
                            "name": agent.name,
                            "role": agent.role,
                            "status": agent.status.value,
                            "progress": agent.progress,
                            "current_task": agent.current_task
                        }
                        for agent in status.agents
                    ],
                    "overall_progress": status.overall_progress,
                    "current_phase": status.current_phase
                }
            })
        
        # Keep connection alive
        while True:
            try:
                await websocket.receive_text()
            except WebSocketDisconnect:
                break
    except WebSocketDisconnect:
        pass
    finally:
        # Remove connection
        orchestrator.remove_websocket_connection(project_id, websocket)


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Not found", "message": str(exc)}


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "An unexpected error occurred"}


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )
