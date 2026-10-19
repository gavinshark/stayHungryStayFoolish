import { create } from 'zustand';
import type { User, ProjectListItem, PaginatedResponse } from '../types';
import api from '../services/api';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, username: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
  clearError: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      await api.login({ email, password });
      const user = await api.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Login failed', isLoading: false });
      throw error;
    }
  },

  register: async (email: string, username: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      await api.register({ email, username, password });
      // After registration, login
      await api.login({ email, password });
      const user = await api.getCurrentUser();
      set({ user, isAuthenticated: true, isLoading: false });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Registration failed', isLoading: false });
      throw error;
    }
  },

  logout: () => {
    api.logout();
    set({ user: null, isAuthenticated: false });
  },

  checkAuth: async () => {
    set({ isLoading: true });
    try {
      if (api.isAuthenticated()) {
        const user = await api.getCurrentUser();
        set({ user, isAuthenticated: true, isLoading: false });
      } else {
        set({ isAuthenticated: false, isLoading: false });
      }
    } catch {
      set({ isAuthenticated: false, isLoading: false });
      api.clearToken();
    }
  },

  clearError: () => set({ error: null }),
}));

interface ProjectState {
  projects: ProjectListItem[];
  totalProjects: number;
  currentPage: number;
  totalPages: number;
  isLoading: boolean;
  error: string | null;
  searchQuery: string;
  sortBy: 'name' | 'health_score' | 'created_at';
  sortOrder: 'asc' | 'desc';
  fetchProjects: (page?: number) => Promise<void>;
  setSearchQuery: (query: string) => void;
  setSorting: (sortBy: 'name' | 'health_score' | 'created_at', sortOrder: 'asc' | 'desc') => void;
  clearError: () => void;
}

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: [],
  totalProjects: 0,
  currentPage: 1,
  totalPages: 1,
  isLoading: false,
  error: null,
  searchQuery: '',
  sortBy: 'health_score',
  sortOrder: 'asc',

  fetchProjects: async (page?: number) => {
    set({ isLoading: true, error: null });
    try {
      const { searchQuery, sortBy, sortOrder } = get();
      const response = await api.getProjects({
        page: page || 1,
        page_size: 20,
        search: searchQuery || undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      set({
        projects: response.items,
        totalProjects: response.total,
        currentPage: response.page,
        totalPages: response.total_pages,
        isLoading: false,
      });
    } catch (error: any) {
      set({ error: error.response?.data?.detail || 'Failed to fetch projects', isLoading: false });
    }
  },

  setSearchQuery: (query: string) => {
    set({ searchQuery: query });
  },

  setSorting: (sortBy: 'name' | 'health_score' | 'created_at', sortOrder: 'asc' | 'desc') => {
    set({ sortBy, sortOrder });
  },

  clearError: () => set({ error: null }),
}));

interface ThemeState {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeState>((set) => ({
  theme: (localStorage.getItem('theme') as 'light' | 'dark') || 'light',
  toggleTheme: () => {
    set((state) => {
      const newTheme = state.theme === 'light' ? 'dark' : 'light';
      localStorage.setItem('theme', newTheme);
      if (newTheme === 'dark') {
        document.documentElement.classList.add('dark');
      } else {
        document.documentElement.classList.remove('dark');
      }
      return { theme: newTheme };
    });
  },
}));