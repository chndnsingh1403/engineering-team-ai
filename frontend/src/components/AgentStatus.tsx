import React from 'react';
import { Agent } from '../types';
import { CheckCircle, Clock, AlertCircle, Loader2 } from 'lucide-react';

interface AgentStatusProps {
  agents: Agent[];
}

export const AgentStatus: React.FC<AgentStatusProps> = ({ agents }) => {
  const getStatusIcon = (status: Agent['status']) => {
    switch (status) {
      case 'idle':
        return <Clock className="h-4 w-4 text-gray-400" />;
      case 'working':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />;
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: Agent['status']) => {
    switch (status) {
      case 'idle':
        return 'text-gray-600';
      case 'working':
        return 'text-blue-600';
      case 'completed':
        return 'text-green-600';
      case 'failed':
        return 'text-red-600';
      default:
        return 'text-gray-600';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Agent Status</h3>
      <div className="space-y-4">
        {agents.map((agent) => (
          <div key={agent.id} className="border border-gray-100 rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center">
                {getStatusIcon(agent.status)}
                <span className="ml-2 font-medium text-gray-900">{agent.name}</span>
              </div>
              <span className={`text-sm font-medium capitalize ${getStatusColor(agent.status)}`}>
                {agent.status}
              </span>
            </div>
            
            <p className="text-sm text-gray-600 mb-2">{agent.role}</p>
            
            {agent.currentTask && (
              <p className="text-sm text-blue-600 mb-2">
                Current task: {agent.currentTask}
              </p>
            )}

            <div className="w-full bg-gray-200 rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all duration-300 ${
                  agent.status === 'completed'
                    ? 'bg-green-500'
                    : agent.status === 'failed'
                    ? 'bg-red-500'
                    : agent.status === 'working'
                    ? 'bg-blue-500'
                    : 'bg-gray-300'
                }`}
                style={{ width: `${agent.progress}%` }}
              />
            </div>
            <p className="text-xs text-gray-500 mt-1">{agent.progress}% complete</p>
          </div>
        ))}
      </div>
    </div>
  );
};
