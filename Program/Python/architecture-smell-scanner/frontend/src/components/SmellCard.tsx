import React from 'react';
import type { Smell, SeverityLevel } from '../types';
import { AlertTriangle, FileCode, Lightbulb } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';

interface SmellCardProps {
  smell: Smell;
  onClick?: () => void;
}

const getSeverityColor = (severity: SeverityLevel): string => {
  switch (severity) {
    case SeverityLevel.CRITICAL:
      return 'border-red-500 bg-red-50 dark:bg-red-900/20';
    case SeverityLevel.HIGH:
      return 'border-orange-500 bg-orange-50 dark:bg-orange-900/20';
    case SeverityLevel.MEDIUM:
      return 'border-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
    case SeverityLevel.LOW:
      return 'border-blue-500 bg-blue-50 dark:bg-blue-900/20';
    default:
      return 'border-gray-300';
  }
};

const getSeverityBadgeColor = (severity: SeverityLevel): string => {
  switch (severity) {
    case SeverityLevel.CRITICAL:
      return 'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200';
    case SeverityLevel.HIGH:
      return 'bg-orange-100 text-orange-800 dark:bg-orange-900 dark:text-orange-200';
    case SeverityLevel.MEDIUM:
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
    case SeverityLevel.LOW:
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const getLanguageForHighlighter = (language: string): string => {
  switch (language) {
    case 'python':
      return 'python';
    case 'java':
      return 'java';
    case 'javascript':
    case 'typescript':
      return 'javascript';
    default:
      return 'text';
  }
};

const SmellCard: React.FC<SmellCardProps> = ({ smell, onClick }) => {
  return (
    <div
      onClick={onClick}
      className={`rounded-lg border-l-4 ${getSeverityColor(smell.severity)} p-4 cursor-pointer hover:shadow-md transition-shadow`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center">
          <AlertTriangle className={`w-5 h-5 mr-2 ${
            smell.severity === SeverityLevel.CRITICAL ? 'text-red-500' :
            smell.severity === SeverityLevel.HIGH ? 'text-orange-500' :
            smell.severity === SeverityLevel.MEDIUM ? 'text-yellow-500' : 'text-blue-500'
          }`} />
          <span className="font-semibold text-gray-900 dark:text-white">{smell.smell_type}</span>
        </div>
        <span className={`px-2 py-1 rounded-full text-xs font-medium ${getSeverityBadgeColor(smell.severity)}`}>
          {smell.severity.toUpperCase()}
        </span>
      </div>

      <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
        {smell.description}
      </p>

      <div className="mt-3 flex items-center text-xs text-gray-500 dark:text-gray-400">
        <FileCode className="w-3 h-3 mr-1" />
        <span className="truncate">{smell.file_path}</span>
        {smell.line_number && (
          <span className="ml-2">Line {smell.line_number}</span>
        )}
      </div>

      {smell.code_snippet && (
        <div className="mt-3 rounded-md overflow-hidden">
          <SyntaxHighlighter
            language={getLanguageForHighlighter(smell.language)}
            style={vscDarkPlus}
            customStyle={{ margin: 0, fontSize: '12px', padding: '0.5rem' }}
          >
            {smell.code_snippet.slice(0, 500)}
          </SyntaxHighlighter>
        </div>
      )}

      {smell.suggestion && (
        <div className="mt-3 flex items-start bg-primary-50 dark:bg-primary-900/20 rounded-md p-2">
          <Lightbulb className="w-4 h-4 text-primary-600 dark:text-primary-400 mr-2 flex-shrink-0 mt-0.5" />
          <p className="text-xs text-gray-600 dark:text-gray-400">
            {smell.suggestion}
          </p>
        </div>
      )}
    </div>
  );
};

export default SmellCard;