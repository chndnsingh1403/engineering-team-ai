import React, { useEffect, useRef } from 'react';
import { Agent, LogEntry, ProcessingStatus } from '../types';
import { 
  CheckCircle, 
  Loader2, 
  Clock, 
  Users, 
  MessageSquare,
  Zap,
  Code,
  TestTube,
  FileText,
  Settings,
  AlertCircle,
  CheckCircle2,
  Wifi
} from 'lucide-react';

interface DetailedProgressTrackerProps {
  processingStatus: ProcessingStatus;
  agents: Agent[];
  logs: LogEntry[];
}

const AGENT_ICONS: { [key: string]: React.ReactNode } = {
  'Lead Architect': <Settings className="w-5 h-5" />,
  'Frontend Developer': <Code className="w-5 h-5" />,
  'Backend Developer': <Zap className="w-5 h-5" />,
  'Test Engineer': <TestTube className="w-5 h-5" />,
  'Documentation Writer': <FileText className="w-5 h-5" />
};

const getStatusColor = (status: string) => {
  switch (status.toLowerCase()) {
    case 'idle': return 'text-gray-500 bg-gray-100';
    case 'working': return 'text-blue-600 bg-blue-100';
    case 'completed': return 'text-green-600 bg-green-100';
    case 'failed': return 'text-red-600 bg-red-100';
    default: return 'text-gray-500 bg-gray-100';
  }
};

const getLogLevelColor = (level: string) => {
  switch (level.toLowerCase()) {
    case 'info': return 'text-blue-600 bg-blue-50 border-blue-200';
    case 'success': return 'text-green-600 bg-green-50 border-green-200';
    case 'warning': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
    case 'error': return 'text-red-600 bg-red-50 border-red-200';
    default: return 'text-gray-600 bg-gray-50 border-gray-200';
  }
};

export const DetailedProgressTracker: React.FC<DetailedProgressTrackerProps> = ({
  processingStatus,
  agents,
  logs
}) => {
  const logsEndRef = useRef<HTMLDivElement>(null);
  
  // Auto-scroll to latest log
  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);
  
  const getPhaseProgress = () => {
    const phase = processingStatus.currentPhase.toLowerCase();
    if (phase.includes('pending')) return 0;
    if (phase.includes('phase 1') || phase.includes('creating system design')) return 20;
    if (phase.includes('phase 2') || phase.includes('developing frontend')) return 40;
    if (phase.includes('phase 3') || phase.includes('developing backend')) return 60;
    if (phase.includes('phase 4') || phase.includes('creating test')) return 80;
    if (phase.includes('phase 5') || phase.includes('creating documentation')) return 90;
    if (phase.includes('completed')) return 100;
    return 0;
  };

  const phaseProgress = getPhaseProgress();
  const recentLogs = logs.slice(-10).reverse();

  return (
    <div className="space-y-6">
      {/* Overall Progress */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-900">Project Progress</h3>
          <span className="text-sm text-gray-600">{phaseProgress}% Complete</span>
        </div>
        
        <div className="w-full bg-gray-200 rounded-full h-3 mb-4">
          <div 
            className="bg-gradient-to-r from-blue-500 to-purple-600 h-3 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${phaseProgress}%` }}
          />
        </div>
        
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-600">Current Phase:</span>
          <span className="font-medium text-gray-900">{processingStatus.currentPhase}</span>
        </div>
      </div>

      {/* Agent Status Cards */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <Users className="w-5 h-5 mr-2" />
          Engineering Team Status
        </h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map((agent) => (
            <div key={agent.id} className="border rounded-lg p-4 hover:shadow-sm transition-shadow">
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  {AGENT_ICONS[agent.name] || <Users className="w-5 h-5" />}
                  <span className="font-medium text-gray-900 text-sm">{agent.name}</span>
                </div>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
              </div>
              
              <p className="text-xs text-gray-600 mb-3">{agent.role}</p>
              
              {agent.currentTask && (
                <div className="mb-3">
                  <p className="text-xs text-gray-700 font-medium mb-1">Current Task:</p>
                  <p className="text-xs text-gray-600">{agent.currentTask}</p>
                </div>
              )}
              
              {agent.progress !== undefined && agent.progress > 0 && (
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs text-gray-600">Progress</span>
                    <span className="text-xs text-gray-700 font-medium">{agent.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-1.5">
                    <div 
                      className="bg-blue-500 h-1.5 rounded-full transition-all duration-300"
                      style={{ width: `${agent.progress}%` }}
                    />
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Real-time Activity Log */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
          <MessageSquare className="w-5 h-5 mr-2" />
          Real-time Activity
        </h3>
        
        <div className="max-h-80 overflow-y-auto space-y-2">
          {recentLogs.length > 0 ? (
            recentLogs.map((log) => (
              <div 
                key={log.id} 
                className={`p-3 rounded-lg border text-sm ${getLogLevelColor(log.level)}`}
              >
                <div className="flex items-start justify-between mb-1">
                  <div className="flex items-center space-x-2">
                    {log.level.toLowerCase() === 'error' && <AlertCircle className="w-4 h-4" />}
                    {log.level.toLowerCase() === 'success' && <CheckCircle2 className="w-4 h-4" />}
                    {log.level.toLowerCase() === 'info' && <MessageSquare className="w-4 h-4" />}
                    <span className="font-medium">{log.agent}</span>
                  </div>
                  <span className="text-xs opacity-75">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                </div>
                <p className="text-sm">{log.message}</p>
              </div>
            ))
          ) : (
            <div className="text-center py-8 text-gray-500">
              <MessageSquare className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <p>No activity logs yet. Logs will appear here as agents start working.</p>
            </div>
          )}
          <div ref={logsEndRef} />
        </div>
      </div>

      {/* Phase Timeline */}
      <div className="bg-white rounded-lg shadow-sm border p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Development Timeline</h3>
        
        <div className="space-y-3">
          {[
            { phase: 'Phase 1: System Design', icon: <Settings className="w-4 h-4" />, progress: phaseProgress >= 20 },
            { phase: 'Phase 2: Frontend Development', icon: <Code className="w-4 h-4" />, progress: phaseProgress >= 40 },
            { phase: 'Phase 3: Backend Development', icon: <Zap className="w-4 h-4" />, progress: phaseProgress >= 60 },
            { phase: 'Phase 4: Test Creation', icon: <TestTube className="w-4 h-4" />, progress: phaseProgress >= 80 },
            { phase: 'Phase 5: Documentation', icon: <FileText className="w-4 h-4" />, progress: phaseProgress >= 90 },
          ].map((item, index) => (
            <div key={index} className="flex items-center space-x-3">
              <div className={`p-2 rounded-full ${item.progress ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'}`}>
                {item.progress ? <CheckCircle className="w-4 h-4" /> : item.icon}
              </div>
              <span className={`text-sm ${item.progress ? 'text-green-600 font-medium' : 'text-gray-600'}`}>
                {item.phase}
              </span>
              {item.progress && <CheckCircle className="w-4 h-4 text-green-500" />}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
