# Python requirements for bls_data_catalog
python_requirements(
    name="reqs",
    resolve="bls_data_catalog_env",
    source="requirements.txt",
)

# Python sources in scripts directory
python_sources(
    name="scripts",
    sources=["scripts/**/*.py"],
    resolve="bls_data_catalog_env",
    dependencies=[":reqs"],
)
