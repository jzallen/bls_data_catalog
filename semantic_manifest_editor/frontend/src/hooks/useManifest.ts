/**
 * Zustand store for manifest state management
 */
import { create } from 'zustand';
import type { SemanticModel } from '../types/manifest';

interface ManifestState {
  semanticModels: SemanticModel[];
  selectedModelId: string | null;

  // Actions
  addSemanticModel: (model: SemanticModel) => void;
  updateSemanticModel: (id: string, model: SemanticModel) => void;
  deleteSemanticModel: (id: string) => void;
  setSelectedModel: (id: string | null) => void;
  clearAll: () => void;
}

export const useManifestStore = create<ManifestState>((set) => ({
  semanticModels: [],
  selectedModelId: null,

  addSemanticModel: (model) => set((state) => ({
    semanticModels: [...state.semanticModels, model]
  })),

  updateSemanticModel: (id, model) => set((state) => ({
    semanticModels: state.semanticModels.map(m =>
      m.name === id ? model : m
    )
  })),

  deleteSemanticModel: (id) => set((state) => ({
    semanticModels: state.semanticModels.filter(m => m.name !== id),
    selectedModelId: state.selectedModelId === id ? null : state.selectedModelId
  })),

  setSelectedModel: (id) => set({ selectedModelId: id }),

  clearAll: () => set({
    semanticModels: [],
    selectedModelId: null
  })
}));
