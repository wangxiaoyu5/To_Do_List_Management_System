export interface User {
  id: string;
  username: string;
  email: string;
  createdAt: string;
}

export interface AuthResponse {
  user: User;
  access: string;
  refresh: string;
}

export interface Category {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

export interface Tag {
  id: string;
  name: string;
  color: string;
  createdAt: string;
}

export type Priority = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Task {
  id: string;
  title: string;
  description?: string;
  priority: Priority;
  dueDate?: string;
  completed: boolean;
  completedAt?: string;
  createdAt: string;
  updatedAt: string;
  categoryId?: string;
  category?: Category;
  tags: Tag[];
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority: Priority;
  dueDate?: string;
  categoryId?: string;
  tagIds: string[];
}

// RAG 相关类型
export interface RAGRecommendationsRequest {
  title: string;
  description?: string;
  priority: Priority;
}

export interface RAGRecommendationsResponse {
  similar_tasks: any[];
  recommendations: {
    suggestions: string[];
    similar_tasks_used?: number;
  };
  has_kb?: boolean;
}

export interface RAGQueryRequest {
  query: string;
}

export interface RAGQueryResponse {
  answer: string;
  related_tasks: any[];
  has_kb?: boolean;
}

export interface RAGChatRequest {
  message: string;
}

export interface RAGChatResponse {
  answer: string;
  context_used: number;
  has_kb?: boolean;
}

export interface RAGStatusResponse {
  has_kb: boolean;
  task_count: number;
  rag_available: boolean;
  collection_name?: string;
  use_openai?: boolean;
  error?: string;
}
