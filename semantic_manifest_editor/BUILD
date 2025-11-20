# Backend PEX Binary
pex_binary(
    name="backend",
    entry_point="uvicorn",
    args=["api.main:app", "--host", "0.0.0.0", "--port", "8000"],
    resolve="semantic_manifest_editor_backend_env",
    dependencies=["backend:lib"],
)

# Backend Docker Image
docker_image(
    name="backend-image",
    instructions=[
        "FROM python:3.12-slim",
        "WORKDIR /app",
        "COPY semantic_manifest_editor/backend.pex /app/backend.pex",
        "EXPOSE 8000",
        'CMD ["/app/backend.pex"]',
    ],
    dependencies=[":backend"],
    image_tags=["latest"],
    repository="semantic-manifest-editor-backend",
)

# Frontend files target
files(
    name="frontend",
    sources=["frontend:lib"],
)

# Frontend Docker Image
docker_image(
    name="frontend-image",
    instructions=[
        "FROM node:18-alpine as build",
        "WORKDIR /app",
        "COPY semantic_manifest_editor/frontend/package*.json ./",
        "RUN npm ci",
        "COPY semantic_manifest_editor/frontend .",
        "RUN npm run build",
        "",
        "FROM nginx:alpine",
        "COPY --from=build /app/dist /usr/share/nginx/html",
        "EXPOSE 80",
        'CMD ["nginx", "-g", "daemon off;"]',
    ],
    dependencies=[":frontend"],
    image_tags=["latest"],
    repository="semantic-manifest-editor-frontend",
)
