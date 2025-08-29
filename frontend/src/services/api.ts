import axios from 'axios';
import { ProjectRequest, ProcessingStatus, ProjectOutput } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  timeout: 30000,
});

export const projectService = {
  // Submit a new project request
  submitProject: async (data: {
    description: string;
    language: string;
    files?: File[];
  }): Promise<ProjectRequest> => {
    const formData = new FormData();
    formData.append('description', data.description);
    formData.append('language', data.language);
    
    if (data.files) {
      data.files.forEach((file) => {
        formData.append('files', file);
      });
    }

    const response = await api.post('/projects/submit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  },

  // Get processing status of a project
  getProjectStatus: async (projectId: string): Promise<ProcessingStatus> => {
    const response = await api.get(`/projects/${projectId}/status`);
    return response.data;
  },

  // Get project output
  getProjectOutput: async (projectId: string): Promise<ProjectOutput> => {
    const response = await api.get(`/projects/${projectId}/output`);
    return response.data;
  },

  // Download project files
  downloadProject: async (projectId: string): Promise<Blob> => {
    const response = await api.get(`/projects/${projectId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },

  // Get all projects
  getAllProjects: async (): Promise<ProjectRequest[]> => {
    const response = await api.get('/projects');
    return response.data;
  },
};

// WebSocket for real-time updates
export const createWebSocketConnection = (
  projectId: string,
  onStatusUpdate: (status: ProcessingStatus) => void
) => {
  const wsUrl = `${API_BASE_URL.replace('http', 'ws')}/ws/${projectId}`;
  const ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      onStatusUpdate(data);
    } catch (error) {
      console.error('Failed to parse WebSocket message:', error);
    }
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  return ws;
};
