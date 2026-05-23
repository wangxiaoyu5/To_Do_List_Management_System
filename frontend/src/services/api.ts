import axios from 'axios';
import type { User, AuthResponse, Category, Tag, Task, TaskFormData } from '../types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('accessToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refresh = localStorage.getItem('refreshToken');
      if (refresh) {
        try {
          const response = await api.post('/auth/token/refresh/', { refresh });
          const { access } = response.data;
          localStorage.setItem('accessToken', access);
          error.config.headers.Authorization = `Bearer ${access}`;
          return api(error.config);
        } catch (e) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: (data: { username: string; email: string; password: string }) =>
    api.post<AuthResponse>('/auth/register/', data),
  login: (data: { username: string; password: string }) =>
    api.post<AuthResponse>('/auth/login/', data),
  getCurrentUser: () => api.get<User>('/auth/user/'),
};

export const categoriesApi = {
  getAll: () => api.get<Category[]>('/categories/'),
  create: (data: { name: string; color?: string }) =>
    api.post<Category>('/categories/', data),
  update: (id: string, data: { name?: string; color?: string }) =>
    api.put<Category>(`/categories/${id}/`, data),
  delete: (id: string) => api.delete(`/categories/${id}/`),
};

export const tagsApi = {
  getAll: () => api.get<Tag[]>('/tags/'),
  create: (data: { name: string; color?: string }) =>
    api.post<Tag>('/tags/', data),
  update: (id: string, data: { name?: string; color?: string }) =>
    api.put<Tag>(`/tags/${id}/`, data),
  delete: (id: string) => api.delete(`/tags/${id}/`),
};

export const tasksApi = {
  getAll: (params?: {
    priority?: string;
    categoryId?: string;
    completed?: string;
    search?: string;
  }) => api.get<Task[]>('/tasks/', { params }),
  getOne: (id: string) => api.get<Task>(`/tasks/${id}/`),
  create: (data: TaskFormData) => api.post<Task>('/tasks/', data),
  update: (id: string, data: Partial<TaskFormData> & { completed?: boolean }) =>
    api.put<Task>(`/tasks/${id}/`, data),
  delete: (id: string) => api.delete(`/tasks/${id}/`),
  toggle: (id: string) => api.patch<Task>(`/tasks/${id}/toggle/`),
};

export const exportApi = {
  exportJSON: () => api.get('/export/json/', { responseType: 'blob' }),
  exportCSV: () => api.get('/export/csv/', { responseType: 'blob' }),
  importJSON: (data: any) => api.post('/import/json/', data),
};

export default api;
