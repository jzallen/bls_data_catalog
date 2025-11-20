/**
 * LocalStorage service for auto-save functionality
 */

const AUTO_SAVE_KEY = 'semantic_manifest_autosave';
const VERSIONS_KEY = 'semantic_manifest_versions';

export interface StoredManifest {
  semantic_models: any[];
  metrics?: any[];
  timestamp: string;
  version: string;
}

export class StorageService {
  /**
   * Save manifest to LocalStorage
   */
  static saveAutoSave(manifest: any): void {
    try {
      const stored: StoredManifest = {
        semantic_models: manifest.semantic_models || [],
        metrics: manifest.metrics || [],
        timestamp: new Date().toISOString(),
        version: '1.0.0'
      };
      localStorage.setItem(AUTO_SAVE_KEY, JSON.stringify(stored));
    } catch (error) {
      console.error('Failed to save to LocalStorage:', error);
    }
  }

  /**
   * Load auto-saved manifest from LocalStorage
   */
  static loadAutoSave(): StoredManifest | null {
    try {
      const stored = localStorage.getItem(AUTO_SAVE_KEY);
      return stored ? JSON.parse(stored) : null;
    } catch (error) {
      console.error('Failed to load from LocalStorage:', error);
      return null;
    }
  }

  /**
   * Clear auto-save
   */
  static clearAutoSave(): void {
    try {
      localStorage.removeItem(AUTO_SAVE_KEY);
    } catch (error) {
      console.error('Failed to clear LocalStorage:', error);
    }
  }

  /**
   * Get storage usage
   */
  static getStorageUsage(): { used: number; total: number } {
    try {
      let used = 0;
      for (const key in localStorage) {
        if (localStorage.hasOwnProperty(key)) {
          used += localStorage[key].length + key.length;
        }
      }
      return {
        used,
        total: 5 * 1024 * 1024 // 5MB typical limit
      };
    } catch (error) {
      return { used: 0, total: 5 * 1024 * 1024 };
    }
  }
}
