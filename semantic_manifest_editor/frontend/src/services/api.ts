/**
 * API client for Semantic Manifest Editor backend
 */
import axios from 'axios';
import type { SemanticModel, ValidationResult } from '../types/manifest';

const apiClient = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const semanticModelsApi = {
  list: () => apiClient.get<SemanticModel[]>('/semantic-models'),
  get: (id: string) => apiClient.get<SemanticModel>(`/semantic-models/${id}`),
  create: (data: SemanticModel) => apiClient.post<SemanticModel>('/semantic-models', data),
  update: (id: string, data: Partial<SemanticModel>) => apiClient.put<SemanticModel>(`/semantic-models/${id}`, data),
  delete: (id: string) => apiClient.delete(`/semantic-models/${id}`),
};

export const validationApi = {
  validateSchema: (manifest: any) => apiClient.post<ValidationResult>('/validation/schema', manifest),
  validateDatabase: (modelId: string) => apiClient.post<ValidationResult>('/validation/database', { semantic_model_id: modelId }),
};

export default apiClient;
