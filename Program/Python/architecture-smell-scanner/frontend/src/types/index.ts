// API Types
export enum SeverityLevel {
  CRITICAL = 'critical',
  HIGH = 'high',
  MEDIUM = 'medium',
  LOW = 'low',
}

export enum ScanStatus {
  PENDING = 'pending',
  RUNNING = 'running',
  COMPLETED = 'completed',
  FAILED = 'failed',
}

export enum ProgrammingLanguage {
  PYTHON = 'python',
  JAVA = 'java',
  JAVASCRIPT = 'javascript',
  TYPESCRIPT = 'typescript',
}

// User types
export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
}

// Project types
export interface Project {
  id: number;
  name: string;
  description: string | null;
  git_url: string | null;
  owner_id: number;
  created_at: string;
  updated_at: string | null;
  code_snapshot_path: string | null;
}

export interface ProjectListItem {
  id: number;
  name: string;
  description: string | null;
  owner_id: number;
  last_scan_health_score: number | null;
  last_scan_date: string | null;
  total_smells: number;
}

export interface Collaborator {
  id: number;
  user_id: number;
  email: string;
  username: string;
  created_at: string;
}

// Scan types
export interface Scan {
  id: number;
  project_id: number;
  status: ScanStatus;
  started_at: string | null;
  completed_at: string | null;
  health_score: number | null;
  total_smells: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
  error_message: string | null;
  created_at: string;
}

export interface ScanDetail extends Scan {
  smells: Smell[];
}

// Smell types
export interface Smell {
  id: number;
  smell_type: string;
  severity: SeverityLevel;
  file_path: string;
  line_number: number | null;
  class_name: string | null;
  method_name: string | null;
  description: string;
  suggestion: string | null;
  code_snippet: string | null;
  language: ProgrammingLanguage;
  created_at: string;
}

// Trend types
export interface TrendDataPoint {
  date: string;
  health_score: number;
  total_smells: number;
  critical_count: number;
  high_count: number;
  medium_count: number;
  low_count: number;
}

export interface TrendData {
  project_id: number;
  project_name: string;
  data_points: TrendDataPoint[];
}

// Pagination
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// API Request types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  username: string;
  password: string;
}

export interface CreateProjectRequest {
  name: string;
  description?: string;
  git_url?: string;
}

export interface CreateScanRequest {
  project_id: number;
}