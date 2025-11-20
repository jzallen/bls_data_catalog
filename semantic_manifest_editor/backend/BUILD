python_requirements(
    name="requirements",
    source="requirements.txt",
    resolve="semantic_manifest_editor_backend_env",
)

python_sources(
    name="backend",
    resolve="semantic_manifest_editor_backend_env",
    dependencies=[":requirements"],
)

pex_binary(
    name="backend-pex",
    entry_point="uvicorn",
    args=["api.main:app", "--host", "0.0.0.0", "--port", "8000"],
    resolve="semantic_manifest_editor_backend_env",
    dependencies=[":backend"],
)
