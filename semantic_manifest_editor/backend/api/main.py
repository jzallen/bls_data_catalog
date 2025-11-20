from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Semantic Manifest Editor API",
    version="1.0.0",
    description="API for creating and editing MetricFlow semantic_manifest.json files"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "semantic-manifest-editor"}

@app.get("/api/semantic-models")
async def list_semantic_models():
    """List all semantic models."""
    return []

@app.get("/api/metrics")
async def list_metrics():
    """List all metrics."""
    return []

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
