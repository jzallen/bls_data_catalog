python_requirements(
    name="requirements",
    source="requirements.txt",
    resolve="bls_data_catalog_env",
)

python_sources(
    name="backend",
    resolve="bls_data_catalog_env",
    dependencies=[":requirements"],
)
