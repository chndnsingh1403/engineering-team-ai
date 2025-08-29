import os
import asyncio
import aiofiles
from typing import Dict, Any, List


async def save_file_async(file_path: str, content: str) -> None:
    """Save file content asynchronously."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
        await f.write(content)


async def read_file_async(file_path: str) -> str:
    """Read file content asynchronously."""
    async with aiofiles.open(file_path, 'r', encoding='utf-8') as f:
        return await f.read()


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe filesystem operations."""
    # Remove or replace unsafe characters
    unsafe_chars = ['<', '>', ':', '"', '|', '?', '*', '/', '\\']
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit length
    if len(filename) > 255:
        filename = filename[:255]
    
    return filename


def extract_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    return os.path.splitext(filename)[1].lower()


def get_file_size_mb(file_path: str) -> float:
    """Get file size in megabytes."""
    if os.path.exists(file_path):
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    return 0.0


async def ensure_directory(directory: str) -> None:
    """Ensure directory exists."""
    os.makedirs(directory, exist_ok=True)


def format_bytes(bytes_value: int) -> str:
    """Format bytes into human readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_value < 1024:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024
    return f"{bytes_value:.1f} TB"


class ProgressTracker:
    """Track progress across multiple tasks."""
    
    def __init__(self, total_tasks: int):
        self.total_tasks = total_tasks
        self.completed_tasks = 0
        self.task_progress: Dict[str, float] = {}
    
    def update_task_progress(self, task_id: str, progress: float):
        """Update progress for a specific task."""
        self.task_progress[task_id] = max(0, min(100, progress))
    
    def complete_task(self, task_id: str):
        """Mark a task as completed."""
        self.task_progress[task_id] = 100
        self.completed_tasks = sum(1 for p in self.task_progress.values() if p >= 100)
    
    def get_overall_progress(self) -> float:
        """Get overall progress percentage."""
        if not self.task_progress:
            return 0
        
        total_progress = sum(self.task_progress.values())
        return total_progress / len(self.task_progress) if self.task_progress else 0
