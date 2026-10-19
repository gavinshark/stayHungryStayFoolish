import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  User,
  AuthToken,
  Project,
  ProjectListItem,
  Collaborator,
  Scan,
  ScanDetail,
  Smell,
  TrendData,
  PaginatedResponse,
  LoginRequest,
  RegisterRequest,
  CreateProjectRequest,
  CreateScanRequest,
  SeverityLevel,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

class ApiService {
  private client: AxiosInstance;
  private token: string | null = null;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to add auth token
    this.client.interceptors.request.use((config) => {
      if (this.token) {
        config.headers.Authorization = `Bearer ${this.token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        if (error.response?.status === 401) {
          this.clearToken();
          window.location.href = '/login';
        }
        return Promise.reject(error);
      }
    );

    // Load token from localStorage on init
    this.token = localStorage.getItem('token');
  }

  setToken(token: string) {
    this.token = token;
    localStorage.setItem('token', token);
  }

  clearToken() {
    this.token = null;
    localStorage.removeItem('token');
  }

  getToken(): string | null {
    return this.token;
  }

  isAuthenticated(): boolean {
    return !!this.token;
  }

  // Auth endpoints
  async register(data: RegisterRequest): Promise<User> {
    const response = await this.client.post<User>('/auth/register', data);
    return response.data;
  }

  async login(data: LoginRequest): Promise<AuthToken> {
    const response = await this.client.post<AuthToken>('/auth/login', data);
    this.setToken(response.data.access_token);
    return response.data;
  }

  async getCurrentUser(): Promise<User> {
    const response = await this.client.get<User>('/auth/me');
    return response.data;
  }

  async logout() {
    this.clearToken();
  }

  // Project endpoints
  async getProjects(params?: {
    page?: number;
    page_size?: number;
    search?: string;
    sort_by?: 'name' | 'health_score' | 'created_at';
    sort_order?: 'asc' | 'desc';
  }): Promise<PaginatedResponse<ProjectListItem>> {
    const response = await this.client.get<PaginatedResponse<ProjectListItem>>('/projects/', { params });
    return response.data;
  }

  async getProject(id: number): Promise<Project> {
    const response = await this.client.get<Project>(`/projects/${id}`);
    return response.data;
  }

  async createProject(data: CreateProjectRequest): Promise<Project> {
    const response = await this.client.post<Project>('/projects/', data);
    return response.data;
  }

  async updateProject(id: number, data: Partial<CreateProjectRequest>): Promise<Project> {
    const response = await this.client.patch<Project>(`/projects/${id}`, data);
    return response.data;
  }

  async deleteProject(id: number): Promise<void> {
    await this.client.delete(`/projects/${id}`);
  }

  async uploadCodeSnapshot(projectId: number, file: File): Promise<Project> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await this.client.post<Project>(
      `/projects/${projectId}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  // Collaborator endpoints
  async addCollaborator(projectId: number, email: string): Promise<Collaborator> {
    const response = await this.client.post<Collaborator>(`/projects/${projectId}/collaborators`, { email });
    return response.data;
  }

  async getCollaborators(projectId: number): Promise<Collaborator[]> {
    const response = await this.client.get<Collaborator[]>(`/projects/${projectId}/collaborators`);
    return response.data;
  }

  async removeCollaborator(projectId: number, collaboratorId: number): Promise<void> {
    await this.client.delete(`/projects/${projectId}/collaborators/${collaboratorId}`);
  }

  // Scan endpoints
  async getProjectScans(projectId: number): Promise<Scan[]> {
    const response = await this.client.get<Scan[]>(`/scans/project/${projectId}`);
    return response.data;
  }

  async getScan(scanId: number): Promise<ScanDetail> {
    const response = await this.client.get<ScanDetail>(`/scans/${scanId}`);
    return response.data;
  }

  async createScan(projectId: number): Promise<Scan> {
    const response = await this.client.post<Scan>('/scans/', { project_id: projectId });
    return response.data;
  }

  async getScanSmells(
    scanId: number,
    filters?: {
      severity?: SeverityLevel;
      smell_type?: string;
    }
  ): Promise<Smell[]> {
    const response = await this.client.get<Smell[]>(`/scans/${scanId}/smells`, { params: filters });
    return response.data;
  }

  async getProjectTrends(projectId: number, days: number = 30): Promise<TrendData> {
    const response = await this.client.get<TrendData>(`/scans/project/${projectId}/trends`, {
      params: { days },
    });
    return response.data;
  }
}

export const api = new ApiService();
export default api;