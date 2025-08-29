import React from 'react';
import { GeneratedFile } from '../types';
import { Code, FileText, TestTube, Book, Palette, Download } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface OutputViewerProps {
  files: GeneratedFile[];
  onDownload?: () => void;
}

export const OutputViewer: React.FC<OutputViewerProps> = ({ files, onDownload }) => {
  const [selectedFile, setSelectedFile] = React.useState<GeneratedFile | null>(
    files.length > 0 ? files[0] : null
  );

  const getFileIcon = (type: GeneratedFile['type']) => {
    switch (type) {
      case 'frontend':
        return <Code className="h-4 w-4 text-blue-500" />;
      case 'backend':
        return <Code className="h-4 w-4 text-green-500" />;
      case 'test':
        return <TestTube className="h-4 w-4 text-purple-500" />;
      case 'documentation':
        return <Book className="h-4 w-4 text-orange-500" />;
      case 'design':
        return <Palette className="h-4 w-4 text-pink-500" />;
      default:
        return <FileText className="h-4 w-4 text-gray-500" />;
    }
  };

  const getFileExtension = (path: string) => {
    return path.split('.').pop()?.toLowerCase() || '';
  };

  const renderFileContent = (file: GeneratedFile) => {
    const extension = getFileExtension(file.path);
    
    if (['md', 'markdown'].includes(extension)) {
      return (
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{file.content}</ReactMarkdown>
        </div>
      );
    }

    if (['js', 'jsx', 'ts', 'tsx', 'py', 'json', 'yaml', 'yml', 'html', 'css'].includes(extension)) {
      return (
        <SyntaxHighlighter
          language={extension === 'jsx' ? 'javascript' : extension === 'tsx' ? 'typescript' : extension}
          style={oneDark}
          className="rounded-lg"
        >
          {file.content}
        </SyntaxHighlighter>
      );
    }

    return (
      <pre className="bg-gray-100 p-4 rounded-lg overflow-x-auto text-sm">
        {file.content}
      </pre>
    );
  };

  if (files.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8 text-center">
        <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
        <p className="text-gray-500">No files generated yet</p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
      <div className="border-b border-gray-200 p-4 flex items-center justify-between">
        <h3 className="text-lg font-semibold text-gray-900">Generated Files</h3>
        {onDownload && (
          <button
            onClick={onDownload}
            className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
          >
            <Download className="h-4 w-4 mr-2" />
            Download All
          </button>
        )}
      </div>

      <div className="flex h-96">
        {/* File list */}
        <div className="w-1/3 border-r border-gray-200 overflow-y-auto">
          {files.map((file, index) => (
            <button
              key={index}
              onClick={() => setSelectedFile(file)}
              className={`w-full text-left p-3 border-b border-gray-100 hover:bg-gray-50 transition-colors ${
                selectedFile?.path === file.path ? 'bg-blue-50 border-r-2 border-r-blue-500' : ''
              }`}
            >
              <div className="flex items-center">
                {getFileIcon(file.type)}
                <span className="ml-2 text-sm font-medium text-gray-900 truncate">
                  {file.path.split('/').pop()}
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-1 capitalize">{file.type}</p>
            </button>
          ))}
        </div>

        {/* File content */}
        <div className="flex-1 overflow-auto">
          {selectedFile ? (
            <div className="p-4">
              <div className="mb-4">
                <h4 className="text-sm font-semibold text-gray-900">{selectedFile.path}</h4>
                <p className="text-xs text-gray-500 capitalize">{selectedFile.type}</p>
              </div>
              {renderFileContent(selectedFile)}
            </div>
          ) : (
            <div className="flex items-center justify-center h-full text-gray-500">
              Select a file to view its content
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
