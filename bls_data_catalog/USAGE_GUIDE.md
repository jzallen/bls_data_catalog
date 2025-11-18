# Usage Guide: BLS Data Catalog Metadata Management System

This guide demonstrates how to use the metadata management system with the BLS employment data example.

## Quick Start

```bash
# Run the setup script
chmod +x setup.sh
./setup.sh

# Or run manually:
python3 scripts/load_sample_data.py
dbt seed --profiles-dir .
dbt run --profiles-dir .
dbt compile --profiles-dir .
python3 scripts/build_metadata_catalog.py
```

## Architecture Overview

```
┌─────────────┐
│ DASHBOARDS  │ - Exposures (collections of reports)
└──────┬──────┘
       │
       ├─────────────────────────────────────┐
       │                                     │
┌──────▼──────┐                      ┌──────▼──────┐
│  REPORTS    │ - Semantic Models    │  REPORTS    │
└──────┬──────┘   (metrics/dims)     └──────┬──────┘
       │                                     │
       ├──────────────┐                      │
       │              │                      │
┌──────▼──────┐ ┌────▼────────┐      ┌──────▼──────┐
│   VIEWS     │ │   VIEWS     │      │   VIEWS     │
└──────┬──────┘ └────┬────────┘      └──────┬──────┘
       │             │                       │
       │             │                       │
┌──────▼──────┐ ┌───▼─────────┐      ┌──────▼──────┐
│   TABLES    │ │   TABLES    │      │   TABLES    │
└─────────────┘ └─────────────┘      └─────────────┘
```

## Layer Definitions

### Layer 1: Tables (dbt sources)
- **Purpose**: Raw data that exists in the warehouse
- **Definition**: `models/sources.yml`
- **Example**: `employment_monthly`, `unemployment_monthly`, `states`
- **No transformations**: Can only be SELECTed by Views

### Layer 2: Views (dbt models)
- **Purpose**: Public interfaces for tables with transformations
- **Definition**: SQL files in `models/views/`
- **Example**: `employment_cleaned.sql`, `state_employment_combined.sql`
- **Relationships**: 1:many with Tables

### Layer 3: Reports (dbt semantic models)
- **Purpose**: On-demand aggregations with metrics and dimensions
- **Definition**: `models/semantic_models.yml`
- **Example**: `state_employment_report`, `regional_employment_report`
- **Relationships**: 1:1 or 1:many with Views

### Layer 4: Dashboards (dbt exposures)
- **Purpose**: Collections of Reports
- **Definition**: `models/exposures.yml`
- **Example**: `labor_market_executive_dashboard`
- **Relationships**: 1:many with Reports

## Using the Metadata Catalog

### 1. Explore the Catalog Programmatically

```python
from scripts.build_metadata_catalog import MetadataCatalog

# Load the catalog
catalog = MetadataCatalog('.')

# List all dashboards
for dashboard_id, dashboard in catalog.dashboards.items():
    print(f"{dashboard.name}: {len(dashboard.reports)} reports")

# Get dashboard lineage
lineage = catalog.get_dashboard_lineage('exposure.bls_data_catalog.labor_market_executive_dashboard')

# Get all reports for a dashboard
reports = catalog.get_reports_for_dashboard('exposure.bls_data_catalog.labor_market_executive_dashboard')
for report in reports:
    print(f"Report: {report.name}")
    print(f"  Dimensions: {[d['name'] for d in report.dimensions]}")
    print(f"  Measures: {[m['name'] for m in report.measures]}")
```

### 2. Query Data via the API

Start the API server:
```bash
python3 scripts/data_delivery_server.py
```

Then use the API:

```bash
# List all dashboards
curl http://localhost:8000/api/dashboards

# Get dashboard metadata
curl http://localhost:8000/api/dashboards/exposure.bls_data_catalog.labor_market_executive_dashboard

# Get dashboard lineage
curl http://localhost:8000/api/dashboards/exposure.bls_data_catalog.labor_market_executive_dashboard/lineage

# Fetch report data
curl -X POST http://localhost:8000/api/reports/state_employment_report/data \
  -H "Content-Type: application/json" \
  -d '{
    "filters": {
      "dimensions": {
        "region_name": ["West", "Northeast"]
      },
      "date_range": {
        "start": "2024-01-01",
        "end": "2024-12-31"
      }
    },
    "group_by": ["region_name", "year_month"],
    "metrics": ["total_employment", "avg_unemployment_rate"]
  }'

# Get all data for a dashboard
curl -X POST http://localhost:8000/api/dashboards/exposure.bls_data_catalog.labor_market_executive_dashboard/data
```

### 3. Query Directly with DuckDB

```bash
duckdb bls_data.duckdb
```

```sql
-- Tables layer: Raw data
SELECT * FROM raw.states LIMIT 5;
SELECT * FROM raw.employment_monthly WHERE state_fips = '06' ORDER BY year_month DESC LIMIT 12;

-- Views layer: Transformed data
SELECT * FROM analytics.employment_cleaned WHERE state_name = 'California' ORDER BY year_month DESC LIMIT 12;
SELECT * FROM analytics.state_employment_combined WHERE region_name = 'West' AND year = 2024;

-- Reports would use MetricFlow (not shown in direct SQL)
```

## Integrating with MetricFlow

To use MetricFlow for query generation (requires dbt 1.6+):

```bash
# Install MetricFlow
pip install metricflow

# Configure MetricFlow
mf setup

# List available metrics
mf list metrics

# Query a metric
mf query \
  --metrics total_employment \
  --group-by state_name,year_month \
  --where "year_month >= '2024-01-01'" \
  --order-by -year_month

# Generate SQL without executing
mf query \
  --metrics total_employment,avg_unemployment_rate \
  --group-by region_name \
  --explain
```

## Micro-Frontend Integration

Example React component that fetches data for a report:

```javascript
// ReportComponent.jsx
import { useEffect, useState } from 'react';

function EmploymentReportChart({ reportId, filters }) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const response = await fetch(
        `http://localhost:8000/api/reports/${reportId}/data`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ filters })
        }
      );
      const result = await response.json();
      setData(result.data);
      setLoading(false);
    }
    
    fetchData();
  }, [reportId, filters]);

  if (loading) return <div>Loading...</div>;

  return (
    <div className="report-chart">
      <h3>{reportId}</h3>
      {/* Render your chart here with data */}
      <pre>{JSON.stringify(data, null, 2)}</pre>
    </div>
  );
}

// Dashboard.jsx
function Dashboard({ dashboardId }) {
  const [metadata, setMetadata] = useState(null);

  useEffect(() => {
    async function fetchMetadata() {
      const response = await fetch(
        `http://localhost:8000/api/dashboards/${dashboardId}`
      );
      const result = await response.json();
      setMetadata(result);
    }
    
    fetchMetadata();
  }, [dashboardId]);

  if (!metadata) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>{metadata.name}</h1>
      <p>{metadata.description}</p>
      
      <div className="reports-grid">
        {metadata.reports.map(report => (
          <EmploymentReportChart
            key={report.id}
            reportId={report.id}
            filters={/* your filters */}
          />
        ))}
      </div>
    </div>
  );
}
```

## CI/CD Integration

Add to your CI/CD pipeline:

```yaml
# .github/workflows/dbt.yml
name: dbt Build and Metadata Update

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install dbt-core dbt-duckdb
      
      - name: Run dbt
        run: |
          dbt deps
          dbt seed --profiles-dir .
          dbt run --profiles-dir .
          dbt compile --profiles-dir .
          dbt test --profiles-dir .
      
      - name: Build metadata catalog
        run: |
          python scripts/build_metadata_catalog.py
      
      - name: Upload metadata artifact
        uses: actions/upload-artifact@v2
        with:
          name: metadata-catalog
          path: target/metadata_catalog.json
```

## Testing the Hierarchy

Verify the relationships:

```python
# test_catalog.py
from scripts.build_metadata_catalog import MetadataCatalog

def test_dashboard_has_reports():
    catalog = MetadataCatalog('.')
    
    # Get a dashboard
    dashboard_id = 'exposure.bls_data_catalog.labor_market_executive_dashboard'
    dashboard = catalog.get_dashboard(dashboard_id)
    
    # Verify it has reports
    assert len(dashboard.reports) > 0
    
    # Verify each report exists
    for report_id in dashboard.reports:
        report = catalog.get_report(report_id)
        assert report is not None
        
        # Verify report has views
        assert len(report.views) > 0
        
        # Verify each view has tables
        for view_id in report.views:
            view = catalog.get_view(view_id)
            assert view is not None
            assert len(view.tables) > 0

def test_lineage_completeness():
    catalog = MetadataCatalog('.')
    
    # Get complete lineage
    lineage = catalog.get_dashboard_lineage(
        'exposure.bls_data_catalog.labor_market_executive_dashboard'
    )
    
    # Verify all layers present
    assert 'dashboard' in lineage
    assert 'reports' in lineage
    assert 'views' in lineage
    assert 'tables' in lineage
    
    # Verify connectivity
    assert len(lineage['reports']) > 0
    assert len(lineage['views']) > 0
    assert len(lineage['tables']) > 0
```

## Next Steps

1. **Add More Reports**: Create additional semantic models in `semantic_models.yml`
2. **Implement MetricFlow**: Integrate full MetricFlow query generation
3. **Add Caching**: Implement Redis or similar for query result caching
4. **Row-Level Security**: Add user context to filter queries
5. **Real-time Updates**: Implement WebSocket connections for live data
6. **Performance Monitoring**: Track query execution times and optimize

## Troubleshooting

### Issue: semantic_manifest.json not found
**Solution**: Ensure you're using dbt 1.6+ and have defined semantic models

### Issue: Reports not linking to views
**Solution**: Check that the `model` field in semantic models matches the `ref()` syntax

### Issue: API returns empty data
**Solution**: Run `dbt seed` and `dbt run` to populate the database

### Issue: Dashboard missing reports
**Solution**: Verify the `meta.reports` list in `exposures.yml` matches semantic model names

## Additional Resources

- [dbt Documentation](https://docs.getdbt.com)
- [dbt-duckdb Adapter](https://github.com/duckdb/dbt-duckdb)
- [MetricFlow Documentation](https://docs.getdbt.com/docs/build/metricflow-overview)
- [DuckDB Documentation](https://duckdb.org/docs/)
