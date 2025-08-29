import React, { useState, useEffect } from 'react';
import { Send, Loader2, Paperclip, Mic, Download } from 'lucide-react';

const PROGRAMMING_LANGUAGES = [
  'JavaScript/TypeScript',
  'Python',
  'Java',
  'C#',
  'Go',
  'Rust',
  'PHP',
  'Ruby',
  'C++',
  'Swift',
  'Kotlin',
  'Other'
];

// API calls
const submitProjectDirect = async (data: { description: string; language: string }) => {
  const formData = new FormData();
  formData.append('description', data.description);
  formData.append('language', data.language);
  
  const response = await fetch('http://localhost:8000/api/projects/submit', {
    method: 'POST',
    body: formData, // Send as FormData, not JSON
  });
  
  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`HTTP error! status: ${response.status} - ${errorText}`);
  }
  
  return response.json();
};

// Get project status
const getProjectStatus = async (projectId: string) => {
  const response = await fetch(`http://localhost:8000/api/projects/${projectId}/status`);
  
  if (!response.ok) {
    throw new Error(`Failed to get status: ${response.status}`);
  }
  
  return response.json();
};

// Download project files
const downloadProject = async (projectId: string) => {
  const response = await fetch(`http://localhost:8000/api/projects/${projectId}/download`);
  
  if (!response.ok) {
    throw new Error(`Failed to download project: ${response.status}`);
  }
  
  return response.blob();
};

export const EngineeringTeamPage: React.FC = () => {
  const [description, setDescription] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('JavaScript/TypeScript');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [status, setStatus] = useState<any>(null);
  const [isPolling, setIsPolling] = useState(false);
  const [isRecording, setIsRecording] = useState(false);

  // Voice recording functionality
  const startVoiceInput = () => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      const recognition = new SpeechRecognition();
      
      recognition.continuous = false;
      recognition.interimResults = false;
      recognition.lang = 'en-US';
      
      recognition.onstart = () => {
        setIsRecording(true);
        console.log('🎤 Voice recording started');
      };
      
      recognition.onresult = (event: any) => {
        const transcript = event.results[0][0].transcript;
        setDescription(prev => prev ? `${prev}\n\n${transcript}` : transcript);
        console.log('🗣️ Voice input:', transcript);
      };
      
      recognition.onerror = (event: any) => {
        console.error('❌ Speech recognition error:', event.error);
        alert('Voice input failed: ' + event.error);
        setIsRecording(false);
      };
      
      recognition.onend = () => {
        setIsRecording(false);
        console.log('🎤 Voice recording ended');
      };
      
      recognition.start();
    } else {
      alert('Voice input not supported in this browser. Please use Chrome or Edge.');
    }
  };

  // File attachment handler
  const handleFileAttachment = () => {
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.multiple = true;
    fileInput.accept = '.txt,.md,.pdf,.docx,.json,.yaml,.yml,.js,.ts,.py,.java,.cpp,.c,.cs,.php,.rb,.go,.rs,.swift,.kt';
    
    fileInput.onchange = (e: any) => {
      const selectedFiles = Array.from(e.target.files || []);
      if (selectedFiles.length > 0) {
        console.log('📎 Files attached:', selectedFiles.map((f: any) => f.name));
        // Here you could handle file preview or storage
        // For now, just add file names to description
        const fileNames = selectedFiles.map((f: any) => f.name).join(', ');
        setDescription(prev => prev ? `${prev}\n\nAttached files: ${fileNames}` : `Attached files: ${fileNames}`);
      }
    };
    
    fileInput.click();
  };

  // Handle project download
  const handleDownload = async () => {
    if (!result?.id) return;

    try {
      console.log('📥 Starting download for project:', result.id);
      const blob = await downloadProject(result.id);
      
      // Create download link
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.style.display = 'none';
      a.href = url;
      a.download = `project-${result.id}.zip`;
      document.body.appendChild(a);
      a.click();
      
      // Cleanup
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
      
      console.log('✅ Download completed successfully');
    } catch (error) {
      console.error('❌ Download failed:', error);
      alert('Failed to download project: ' + (error instanceof Error ? error.message : 'Unknown error'));
    }
  };

  // Polling effect for status updates
  useEffect(() => {
    let pollInterval: number;
    
    if (result?.id && isPolling) {
      console.log('🔄 Starting status polling for project:', result.id);
      
      const pollStatus = async () => {
        try {
          const statusResponse = await getProjectStatus(result.id);
          console.log('📊 Status update:', statusResponse);
          
          // Handle error responses gracefully
          if (statusResponse.error) {
            console.log('⚠️ Status error:', statusResponse.error);
            if (statusResponse.error.includes('not found')) {
              // Project might still be initializing, continue polling
              return;
            }
          }
          
          setStatus(statusResponse);
          
          // Stop polling if completed or failed
          if (statusResponse.currentPhase === 'Completed' || 
              statusResponse.currentPhase === 'Failed' ||
              statusResponse.currentPhase?.includes('Complete')) {
            console.log('✅ Polling complete');
            setIsPolling(false);
          }
        } catch (error) {
          console.error('❌ Failed to poll status:', error);
          // Don't stop polling on network errors, just log them
        }
      };
      
      // Initial poll
      pollStatus();
      
      // Poll every 2 seconds
      pollInterval = window.setInterval(pollStatus, 2000);
    }
    
    return () => {
      if (pollInterval) {
        window.clearInterval(pollInterval);
      }
    };
  }, [result?.id, isPolling]);

  const handleButtonClick = async () => {
    console.log('🔥 DIRECT BUTTON CLICK - NO FORM BEHAVIOR');
    
    if (!description.trim()) {
      alert('Please enter a description');
      return;
    }

    if (isSubmitting) {
      console.log('Already submitting...');
      return;
    }

    setIsSubmitting(true);
    setError('');
    
    try {
      console.log('📡 Making direct fetch call...');
      
      const project = await submitProjectDirect({
        description: description.trim(),
        language: selectedLanguage,
      });
      
      console.log('✅ SUCCESS:', project);
      setResult(project);
      setDescription(''); // Clear form
      
      // Start polling for status updates after a brief delay
      console.log('🚀 Starting automatic status polling in 2 seconds...');
      setTimeout(() => {
        setIsPolling(true);
      }, 2000); // Give the backend 2 seconds to start processing
      setError(''); // Clear any previous errors
      
    } catch (err) {
      console.error('❌ ERROR:', err);
      const errorMsg = err instanceof Error ? err.message : 'Unknown error';
      setError(errorMsg);
      
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-2xl mx-auto">
        <div className="bg-white rounded-lg shadow p-6">
          <h1 className="text-2xl font-bold mb-6">Agentic Engineering Team</h1>
          
          {/* Simple Input Fields - NO FORM WRAPPER */}
          <div className="space-y-4 mb-6">
            <div>
              <label className="block text-sm font-medium mb-2">
                Project Description *
              </label>
              <div className="relative">
                <textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  rows={4}
                  className="w-full border border-gray-300 rounded px-3 py-2 pr-20"
                  placeholder="Describe your project..."
                  disabled={isSubmitting}
                />
                
                {/* Corner Icons */}
                <div className="absolute bottom-2 right-2 flex space-x-1">
                  {/* File Attachment Icon */}
                  <button
                    type="button"
                    onClick={handleFileAttachment}
                    disabled={isSubmitting}
                    className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded transition-colors"
                    title="Attach files"
                    aria-label="Attach files"
                  >
                    <Paperclip className="h-4 w-4" />
                  </button>
                  
                  {/* Voice Input Icon */}
                  <button
                    type="button"
                    onClick={startVoiceInput}
                    disabled={isSubmitting}
                    className={`p-1.5 rounded transition-colors ${
                      isRecording 
                        ? 'text-red-500 bg-red-50 animate-pulse' 
                        : 'text-gray-400 hover:text-gray-600 hover:bg-gray-100'
                    }`}
                    title={isRecording ? 'Recording... (speak now)' : 'Voice input'}
                    aria-label={isRecording ? 'Recording voice input' : 'Start voice input'}
                  >
                    <Mic className="h-4 w-4" />
                  </button>
                </div>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">
                Programming Language
              </label>
              <select
                value={selectedLanguage}
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2"
                disabled={isSubmitting}
              >
                {PROGRAMMING_LANGUAGES.map((lang) => (
                  <option key={lang} value={lang}>
                    {lang}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Direct Button - NO FORM BEHAVIOR */}
          <div className="mb-6">
            <button
              type="button"
              onClick={handleButtonClick}
              disabled={isSubmitting || !description.trim()}
              className={`
                w-full py-3 px-4 rounded font-medium flex items-center justify-center space-x-2
                ${isSubmitting || !description.trim()
                  ? 'bg-gray-400 text-gray-600 cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700 cursor-pointer'
                }
              `}
            >
              {isSubmitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Submitting...</span>
                </>
              ) : (
                <>
                  <Send className="h-4 w-4" />
                  <span>Submit Project</span>
                </>
              )}
            </button>
          </div>

          {/* Results */}
          {error && (
            <div className="bg-red-50 border border-red-200 rounded p-4 mb-4">
              <h3 className="font-medium text-red-800">Error</h3>
              <p className="text-red-600 text-sm">{error}</p>
            </div>
          )}

          {result && (
            <div className="bg-green-50 border border-green-200 rounded p-4">
              <h3 className="font-medium text-green-800">Project Submitted Successfully!</h3>
              <div className="text-sm text-green-600 mt-2 space-y-2">
                <div><strong>Project ID:</strong> {result.id}</div>
                <div><strong>Status:</strong> {result.status}</div>
                <div><strong>Language:</strong> {result.language}</div>
                
                {/* Real-time status updates */}
                {status && (
                  <div className="mt-4 p-3 bg-blue-50 border border-blue-200 rounded">
                    <h4 className="font-medium text-blue-800 mb-2">Live Progress:</h4>
                    <div><strong>Phase:</strong> {status.currentPhase || 'Starting...'}</div>
                    <div><strong>Progress:</strong> {status.overallProgress || 0}%</div>
                    
                    {status.agents && status.agents.length > 0 && (
                      <div className="mt-2">
                        <strong>Active Agents:</strong>
                        <div className="text-xs mt-1">
                          {status.agents.map((agent: any, idx: number) => (
                            <div key={idx} className="flex justify-between">
                              <span>{agent.name}</span>
                              <span className={`px-2 py-1 rounded text-xs ${
                                agent.status === 'active' ? 'bg-green-100 text-green-800' :
                                agent.status === 'processing' ? 'bg-blue-100 text-blue-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {agent.status}
                              </span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {isPolling && (
                      <div className="mt-2 text-xs text-blue-600 flex items-center">
                        <Loader2 className="h-3 w-3 animate-spin mr-1" />
                        Live updates active...
                      </div>
                    )}
                  </div>
                )}
                
                {/* Download button when project is completed */}
                {status && (status.currentPhase === 'Completed' || status.currentPhase?.includes('Complete')) && (
                  <div className="mt-4 pt-4 border-t border-green-200">
                    <button
                      onClick={handleDownload}
                      className="w-full bg-green-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-green-700 transition-colors flex items-center justify-center space-x-2"
                    >
                      <Download className="h-4 w-4" />
                      <span>Download Project Files</span>
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
