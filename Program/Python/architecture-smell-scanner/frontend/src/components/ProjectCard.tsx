import React from 'react';
import { Link } from 'react-router-dom';
import type { ProjectListItem } from '../types';
import { format } from 'date-fns';
import { Activity, AlertTriangle, Clock, ArrowRight } from 'lucide-react';

interface ProjectCardProps {
  project: ProjectListItem;
}

const getHealthScoreColor = (score: number | null): string => {
  if (score === null) return 'text-gray-500';
  if (score >= 80) return 'text-green-500';
  if (score >= 60) return 'text-yellow-500';
  if (score >= 40) return 'text-orange-500';
  return 'text-red-500';
};

const getHealthScoreBg = (score: number | null): string => {
  if (score === null) return 'bg-gray-100 dark:bg-gray-800';
  if (score >= 80) return 'bg-green-50 dark:bg-green-900/20';
  if (score >= 60) return 'bg-yellow-50 dark:bg-yellow-900/20';
  if (score >= 40) return 'bg-orange-50 dark:bg-orange-900/20';
  return 'bg-red-50 dark:bg-red-900/20';
};

const ProjectCard: React.FC<ProjectCardProps> = ({ project }) => {
  return (
    <Link
      to={`/projects/${project.id}`}
      className="block bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow duration-200"
    >
      <div className="p-5">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white truncate">
              {project.name}
            </h3>
            {project.description && (
              <p className="mt-1 text-sm text-gray-500 dark:text-gray-400 line-clamp-2">
                {project.description}
              </p>
            )}
          </div>
          
          {/* Health Score Badge */}
          <div className={`ml-4 flex-shrink-0 ${getHealthScoreBg(project.last_scan_health_score)} rounded-lg px-3 py-2`}>
            <div className={`text-2xl font-bold ${getHealthScoreColor(project.last_scan_health_score)}`}>
              {project.last_scan_health_score ?? '-'}
            </div>
            <div className="text-xs text-gray-500 dark:text-gray-400 text-center">Score</div>
          </div>
        </div>

        <div className="mt-4 flex items-center justify-between text-sm">
          <div className="flex items-center space-x-4">
            {project.total_smells > 0 && (
              <div className="flex items-center text-gray-600 dark:text-gray-400">
                <AlertTriangle className="w-4 h-4 mr-1" />
                <span>{project.total_smells} smells</span>
              </div>
            )}
            {project.last_scan_date && (
              <div className="flex items-center text-gray-500 dark:text-gray-500">
                <Clock className="w-4 h-4 mr-1" />
                <span>{format(new Date(project.last_scan_date), 'MMM d, yyyy')}</span>
              </div>
            )}
          </div>
          <ArrowRight className="w-4 h-4 text-gray-400" />
        </div>
      </div>
    </Link>
  );
};

export default ProjectCard;