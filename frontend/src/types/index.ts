export interface ProjectRequest {
  id: string;
  description: string;
  language: string;
  attachments?: File[];
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: Date;
  completedAt?: Date;
}

export interface Agent {
  id: string;
  name: string;
  role: string;
  status: 'idle' | 'working' | 'completed' | 'failed';
  progress: number;
  currentTask?: string;
  output?: string;
}

export interface ProcessingStatus {
  requestId: string;
  agents: Agent[];
  overallProgress: number;
  currentPhase: string;
  logs: LogEntry[];
}

export interface LogEntry {
  id: string;
  timestamp: Date;
  agent: string;
  level: 'info' | 'warning' | 'error' | 'success';
  message: string;
}

export interface GeneratedFile {
  path: string;
  content: string;
  type: 'frontend' | 'backend' | 'test' | 'documentation' | 'design';
}

export interface ProjectOutput {
  requestId: string;
  files: GeneratedFile[];
  downloadUrl?: string;
  summary: string;
}
