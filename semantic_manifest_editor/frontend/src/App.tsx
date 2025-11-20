/**
 * Main App component for Semantic Manifest Editor
 */
import { useState, useEffect } from 'react';
import { useManifestStore } from './hooks/useManifest';
import { semanticModelsApi } from './services/api';
import './App.css';

function App() {
  const { semanticModels, addSemanticModel } = useManifestStore();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await semanticModelsApi.list();
        setLoading(false);
      } catch (err: any) {
        setError(err.message || 'Failed to load data');
        setLoading(false);
      }
    }
    fetchData();
  }, []);

  if (loading) return <div className="app-loading">Loading Semantic Manifest Editor...</div>;
  if (error) return <div className="app-error">Error: {error}</div>;

  return (
    <div className="app">
      <header className="app-header">
        <h1>Semantic Manifest Editor</h1>
        <div className="app-actions">
          <button className="btn-primary">Create Semantic Model</button>
          <button className="btn-secondary">Export Manifest</button>
        </div>
      </header>

      <main className="app-main">
        <div className="models-list">
          <h2>Semantic Models ({semanticModels.length})</h2>
          {semanticModels.length === 0 ? (
            <p className="empty-state">No semantic models yet. Create one to get started.</p>
          ) : (
            <ul>
              {semanticModels.map((model) => (
                <li key={model.name}>
                  <strong>{model.name}</strong>
                  {model.description && <p>{model.description}</p>}
                  <small>
                    {model.entities.length} entities, {model.dimensions.length} dimensions, {model.measures.length} measures
                  </small>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
