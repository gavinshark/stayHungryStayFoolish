import React, { useEffect, useState } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import type { Project, Scan, ScanDetail, Smell, TrendData, SeverityLevel } from '../types';
import api from '../services/api';
import SmellCard from '../components/SmellCard';
import HealthChart from '../components/HealthChart';
import { useThemeStore } from '../store';
import { format } from 'date-fns';
import { 
  ArrowLeft, 
  Play, 
  RefreshCw, 
  Clock, 
  AlertTriangle, 
  Activity,
  FileCode,
  Users,
  Download,
  Share2,
  ChevronDown,
  ChevronUp,
  Upload
} from 'lucide-react';

const ProjectDetailPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { theme } = useThemeStore();
  
  const [project, setProject] = useState<Project | null>(null);
  const [scans, setScans] = useState<Scan[]>([]);
  const [currentScan, setCurrentScan] = useState<ScanDetail | null>(null);
  const [trendData, setTrendData] = useState<TrendData | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isScanning, setIsScanning] = useState(false);
  const [error, setError] = useState('');
  
  // Filters
  const [severityFilter, setSeverityFilter] = useState<SeverityLevel | ''>('');
  const [typeFilter, setTypeFilter] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [showUploadModal, setShowUploadModal] = useState(false);

  useEffect(() => {
    if (projectId) {
      loadProjectData();
    }
  }, [projectId]);

  const loadProjectData = async () => {
    if (!projectId) return;
    setIsLoading(true);
    try {
      const [projectData, scansData, trendsData] = await Promise.all([
        api.getProject(parseInt(projectId)),
        api.getProjectScans(parseInt(projectId)),
        api.getProjectTrends(parseInt(projectId), 30),
      ]);
      setProject(projectData);
      setScans(scansData);
      setTrendData(trendsData);
      
      // Load most recent completed scan details
      const latestCompleted = scansData.find((s) => s.status === 'completed');
      if (latestCompleted) {
        const scanDetail = await api.getScan(latestCompleted.id);
        setCurrentScan(scanDetail);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load project');
    } finally {
      setIsLoading(false);
    }
  };

  const handleStartScan = async () => {
    if (!projectId) return;
    setIsScanning(true);
    try {
      const scan = await api.createScan(parseInt(projectId));
      setScans((prev) => [scan, ...prev]);
      
      // Poll for completion
      pollScanStatus(scan.id);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to start scan');
      setIsScanning(false);
    }
  };

  const pollScanStatus = async (scanId: number) => {
    const poll = async () => {
      try {
        const scan = await api.getScan(scanId);
        setScans((prev) => prev.map((s) => s.id === scanId ? scan : s));
        
        if (scan.status === 'completed') {
          setCurrentScan(scan);
          setIsScanning(false);
          // Refresh trends
          const trends = await api.getProjectTrends(parseInt(projectId!), 30);
          setTrendData(trends);
        } else if (scan.status === 'failed') {
          setIsScanning(false);
          setError('Scan failed. Please check your code repository.');
        } else {
          setTimeout(poll, 2000);
        }
      } catch {
        setTimeout(poll, 2000);
      }
    };
    poll();
  };

  const filteredSmells = currentScan?.smells.filter((smell) => {
    if (severityFilter && smell.severity !== severityFilter) return false;
    if (typeFilter && smell.smell_type !== typeFilter) return false;
    return true;
  }) || [];

  const uniqueSmellTypes = [...new Set(currentScan?.smells.map((s) => s.smell_type) || [])];

  const getSeverityCounts = () => {
    if (!currentScan) return { critical: 0, high: 0, medium: 0, low: 0 };
    return {
      critical: currentScan.critical_count,
      high: currentScan.high_count,
      medium: currentScan.medium_count,
      low: currentScan.low_count,
    };
  };

  const counts = getSeverityCounts();

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-8 h-8 border-4 border-primary-600 border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!project) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-500">Project not found</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="mr-4 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {project.name}
                </h1>
                {project.description && (
                  <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
                    {project.description}
                  </p>
                )}
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <button
                onClick={() => setShowUploadModal(true)}
                className="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
              >
                <Upload className="w-4 h-4 mr-2" />
                Upload Code
              </button>
              <button
                onClick={handleStartScan}
                disabled={isScanning}
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
              >
                {isScanning ? (
                  <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                ) : (
                  <Play className="w-4 h-4 mr-2" />
                )}
                {isScanning ? 'Scanning...' : 'Run Scan'}
              </button>
            </div>
          </div>

          {/* Stats Overview */}
          {currentScan && (
            <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
              <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-4">
                <div className="text-3xl font-bold text-gray-900 dark:text-white">
                  {currentScan.health_score ?? '-'}
                </div>
                <div className="text-sm text-gray-500 dark:text-gray-400">Health Score</div>
              </div>
              <div className="bg-red-50 dark:bg-red-900/20 rounded-lg p-4">
                <div className="text-3xl font-bold text-red-600">{counts.critical}</div>
                <div className="text-sm text-red-600">Critical</div>
              </div>
              <div className="bg-orange-50 dark:bg-orange-900/20 rounded-lg p-4">
                <div className="text-3xl font-bold text-orange-600">{counts.high}</div>
                <div className="text-sm text-orange-600">High</div>
              </div>
              <div className="bg-yellow-50 dark:bg-yellow-900/20 rounded-lg p-4">
                <div className="text-3xl font-bold text-yellow-600">{counts.medium}</div>
                <div className="text-sm text-yellow-600">Medium</div>
              </div>
              <div className="bg-blue-50 dark:bg-blue-900/20 rounded-lg p-4">
                <div className="text-3xl font-bold text-blue-600">{counts.low}</div>
                <div className="text-sm text-blue-600">Low</div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 dark:bg-red-900/20 border border-red-200 rounded-md p-4">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        <div className="grid gap-8 lg:grid-cols-3">
          {/* Main Content - Smells */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white">
                  Architecture Smells
                </h2>
                <button
                  onClick={() => setShowFilters(!showFilters)}
                  className="text-sm text-primary-600 hover:text-primary-500 flex items-center"
                >
                  Filters
                  {showFilters ? <ChevronUp className="w-4 h-4 ml-1" /> : <ChevronDown className="w-4 h-4 ml-1" />}
                </button>
              </div>

              {showFilters && (
                <div className="mb-4 flex gap-4">
                  <select
                    value={severityFilter}
                    onChange={(e) => setSeverityFilter(e.target.value as SeverityLevel | '')}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white"
                  >
                    <option value="">All Severities</option>
                    <option value="critical">Critical</option>
                    <option value="high">High</option>
                    <option value="medium">Medium</option>
                    <option value="low">Low</option>
                  </select>
                  <select
                    value={typeFilter}
                    onChange={(e) => setTypeFilter(e.target.value)}
                    className="px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm dark:bg-gray-700 dark:text-white"
                  >
                    <option value="">All Types</option>
                    {uniqueSmellTypes.map((type) => (
                      <option key={type} value={type}>{type}</option>
                    ))}
                  </select>
                </div>
              )}

              {!currentScan ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  <FileCode className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No scan data available. Run a scan to see results.</p>
                </div>
              ) : filteredSmells.length === 0 ? (
                <div className="text-center py-8 text-gray-500 dark:text-gray-400">
                  <Activity className="w-12 h-12 mx-auto mb-4 opacity-50" />
                  <p>No smells match your filters.</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {filteredSmells.map((smell) => (
                    <SmellCard key={smell.id} smell={smell} />
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Trend Chart */}
            {trendData && trendData.data_points.length > 0 && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
                <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                  Health Trend (30 days)
                </h2>
                <HealthChart data={trendData} isDark={theme === 'dark'} />
              </div>
            )}

            {/* Recent Scans */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Recent Scans
              </h2>
              {scans.length === 0 ? (
                <p className="text-sm text-gray-500 dark:text-gray-400">No scans yet</p>
              ) : (
                <div className="space-y-3">
                  {scans.slice(0, 5).map((scan) => (
                    <div
                      key={scan.id}
                      className="flex items-center justify-between text-sm border-b border-gray-100 dark:border-gray-700 pb-2"
                    >
                      <div className="flex items-center">
                        {scan.status === 'completed' && (
                          <span className="w-2 h-2 bg-green-500 rounded-full mr-2" />
                        )}
                        {scan.status === 'running' && (
                          <RefreshCw className="w-3 h-3 text-blue-500 animate-spin mr-2" />
                        )}
                        {scan.status === 'failed' && (
                          <span className="w-2 h-2 bg-red-500 rounded-full mr-2" />
                        )}
                        <span className="text-gray-700 dark:text-gray-300">
                          {format(new Date(scan.created_at), 'MMM d, h:mm a')}
                        </span>
                      </div>
                      <span className="text-gray-500 dark:text-gray-400">
                        {scan.health_score ?? '...'}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Actions */}
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700 p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
                Actions
              </h2>
              <div className="space-y-2">
                <button className="w-full flex items-center px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md">
                  <Download className="w-4 h-4 mr-2" />
                  Export Report (PDF)
                </button>
                <button className="w-full flex items-center px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md">
                  <Download className="w-4 h-4 mr-2" />
                  Export Trends (CSV)
                </button>
                <button className="w-full flex items-center px-3 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md">
                  <Share2 className="w-4 h-4 mr-2" />
                  Generate Share Link
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Upload Modal */}
      {showUploadModal && (
        <UploadModal 
          projectId={parseInt(projectId!)} 
          onClose={() => setShowUploadModal(false)} 
          onUpload={loadProjectData}
        />
      )}
    </div>
  );
};

const UploadModal: React.FC<{ projectId: number; onClose: () => void; onUpload: () => void }> = ({
  projectId,
  onClose,
  onUpload,
}) => {
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState('');

  const handleUpload = async () => {
    if (!file) return;
    setIsUploading(true);
    setError('');
    
    try {
      await api.uploadCodeSnapshot(projectId, file);
      onUpload();
      onClose();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      <div className="absolute inset-0 bg-black/50" onClick={onClose} />
      <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full mx-4 p-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
          Upload Code Snapshot
        </h2>

        {error && (
          <div className="mb-4 bg-red-50 dark:bg-red-900/20 border border-red-200 rounded-md p-3">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center">
          <input
            type="file"
            accept=".zip,.tar,.gz"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="hidden"
            id="code-upload"
          />
          <label
            htmlFor="code-upload"
            className="cursor-pointer"
          >
            <Upload className="w-10 h-10 mx-auto text-gray-400 mb-2" />
            <p className="text-sm text-gray-600 dark:text-gray-400">
              {file ? file.name : 'Click to select a code archive'}
            </p>
            <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">
              ZIP, TAR, or GZ (max 100MB)
            </p>
          </label>
        </div>

        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700"
          >
            Cancel
          </button>
          <button
            onClick={handleUpload}
            disabled={!file || isUploading}
            className="px-4 py-2 bg-primary-600 hover:bg-primary-700 rounded-md text-sm font-medium text-white disabled:opacity-50"
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProjectDetailPage;