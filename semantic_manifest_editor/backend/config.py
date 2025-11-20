"""Configuration for Semantic Manifest Editor backend."""
import duckdb
from pathlib import Path

# DuckDB connection configuration
DB_PATH = "/workspaces/bls_data_catalog/bls_data.duckdb"


def get_db_connection(read_only: bool = True) -> duckdb.DuckDBPyConnection:
    """Get DuckDB connection for validation queries.

    Args:
        read_only: Whether to open in read-only mode (default: True for safety)

    Returns:
        DuckDB connection object
    """
    db_file = Path(DB_PATH)
    if not db_file.exists():
        raise FileNotFoundError(f"DuckDB file not found: {DB_PATH}")

    return duckdb.connect(str(db_file), read_only=read_only)
