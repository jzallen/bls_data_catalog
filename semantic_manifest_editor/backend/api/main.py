from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import semantic_models

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

# Register routers
app.include_router(semantic_models.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "semantic-manifest-editor"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
