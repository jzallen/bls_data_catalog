# BLS Employment Data Catalog Example

This is a complete example of a data catalog metadata management system using dbt with DuckDB, demonstrating the four abstraction layers:

1. **Tables** (dbt sources) - Raw BLS data
2. **Views** (dbt models) - Cleaned and transformed data
3. **Reports** (dbt semantic models) - Aggregations and metrics
4. **Dashboards** (dbt exposures) - Collections of reports

## Data Source

This example fetches real data from the BLS (Bureau of Labor Statistics) Public Data API:
- **Employment levels by state** (LAUS Measure 03)
- **Unemployment rates by state** (LAUS Measure 04)
- **Labor force by state** (LAUS Measure 05)
- **Unemployed counts by state** (LAUS Measure 06)
- **State metadata** (FIPS codes, regions, divisions)

Data is fetched for all 51 states (50 states + DC) for the last 3 years.

## Project Structure

```
bls_data_catalog/
├── dbt_project.yml
├── profiles.yml
├── bls_data.duckdb              # DuckDB database (created by load script)
├── models/
│   ├── sources.yml              # Tables layer
│   ├── views/                   # Views layer
│   │   ├── employment_cleaned.sql
│   │   ├── unemployment_cleaned.sql
│   │   └── state_employment_combined.sql
│   ├── semantic_models.yml      # Reports layer
│   └── exposures.yml            # Dashboards layer
└── scripts/
    ├── load_sample_data.py      # Fetch real BLS data via API
    ├── build_metadata_catalog.py
    └── data_delivery_server.py
```

## Setup

1. Install dependencies:
```bash
pip install dbt-core dbt-duckdb requests
```

2. Fetch real BLS data and load into DuckDB:
```bash
python scripts/load_sample_data.py
```

This will:
- Fetch 3 years of LAUS data from the BLS Public Data API
- Create `bls_data.duckdb` with raw employment, unemployment, and state data
- No API key required (uses unauthenticated access)

3. Run dbt to build analytics views:
```bash
dbt deps
dbt run
dbt compile
```

Note: `dbt seed` is no longer needed since data is loaded directly to DuckDB by the load script.

4. The compiled metadata will be in `target/manifest.json` and `target/semantic_manifest.json`

## Query Examples

After running dbt, you can query the semantic models using MetricFlow:

```bash
# Get unemployment rate by region for last quarter
mf query --metrics unemployment_rate --group-by region_name,year_month --where "year_month >= '2024-07-01'"

# Get employment growth by state
mf query --metrics employment_growth_pct --group-by state_name --order-by -employment_growth_pct
```

## API Usage

The metadata store can be built by parsing the compiled dbt artifacts, then used to generate queries dynamically for each report in a dashboard.
