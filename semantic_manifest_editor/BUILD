# Backend Docker Image
docker_image(
    name="backend-image",
    instructions=[
        "FROM python:3.12-slim",
        "WORKDIR /app",
        "COPY semantic_manifest_editor/backend/requirements.txt .",
        "RUN pip install --no-cache-dir -r requirements.txt",
        "COPY semantic_manifest_editor/backend .",
        "EXPOSE 8000",
        'CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]',
    ],
    dependencies=[
        "semantic_manifest_editor/backend:backend",
    ],
    image_tags=["latest"],
    repository="semantic-manifest-editor-backend",
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
    dependencies=[
        "semantic_manifest_editor/frontend:frontend",
    ],
    image_tags=["latest"],
    repository="semantic-manifest-editor-frontend",
)
