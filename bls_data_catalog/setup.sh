#!/bin/bash
# Setup script for BLS Data Catalog example

set -e

echo "=================================================="
echo "BLS Data Catalog Setup"
echo "=================================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "✓ Virtual environment created"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install dbt-core dbt-duckdb fastapi uvicorn[standard] duckdb

echo "✓ Dependencies installed"

# Generate sample data
echo ""
echo "Generating sample BLS data..."
python3 scripts/load_sample_data.py

echo "✓ Sample data generated"

# Run dbt
echo ""
echo "Running dbt..."
dbt deps
dbt seed --profiles-dir .
dbt run --profiles-dir .
dbt compile --profiles-dir .

echo "✓ dbt models compiled"

# Build metadata catalog
echo ""
echo "Building metadata catalog..."
python3 scripts/build_metadata_catalog.py

echo "✓ Metadata catalog built"

echo ""
echo "=================================================="
echo "Setup complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo ""
echo "1. View the metadata catalog:"
echo "   cat target/metadata_catalog.json | jq"
echo ""
echo "2. Query the data with DuckDB CLI:"
echo "   duckdb bls_data.duckdb"
echo "   SELECT * FROM analytics.state_employment_combined LIMIT 5;"
echo ""
echo "3. Start the data delivery API server:"
echo "   python3 scripts/data_delivery_server.py"
echo ""
echo "4. View API docs:"
echo "   Open http://localhost:8000/docs in your browser"
echo ""
