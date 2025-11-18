# BLS Employment Data Catalog Example

This is a complete example of a data catalog metadata management system using dbt with DuckDB, demonstrating the four abstraction layers:

1. **Tables** (dbt sources) - Raw BLS data
2. **Views** (dbt models) - Cleaned and transformed data
3. **Reports** (dbt semantic models) - Aggregations and metrics
4. **Dashboards** (dbt exposures) - Collections of reports

## Data Source

This example uses publicly available BLS (Bureau of Labor Statistics) data:
- **Employment levels by state** (from Local Area Unemployment Statistics)
- **Unemployment rates by state** (from LAUS)
- **State metadata** (FIPS codes, regions, divisions)

## Project Structure

```
bls_data_catalog/
├── dbt_project.yml
├── profiles.yml
├── data/                          # Seed files with sample BLS data
│   ├── states.csv
│   ├── employment_monthly.csv
│   └── unemployment_monthly.csv
├── models/
│   ├── sources.yml                # Tables layer
│   ├── views/                     # Views layer
│   │   ├── employment_cleaned.sql
│   │   ├── unemployment_cleaned.sql
│   │   └── state_employment_combined.sql
│   ├── semantic_models.yml        # Reports layer
│   └── exposures.yml              # Dashboards layer
└── scripts/
    └── load_sample_data.py        # Generate sample BLS-like data
```

## Setup

1. Install dependencies:
```bash
pip install dbt-core dbt-duckdb
```

2. Initialize the DuckDB database with sample data:
```bash
python scripts/load_sample_data.py
```

3. Run dbt:
```bash
dbt deps
dbt seed
dbt run
dbt compile
```

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
