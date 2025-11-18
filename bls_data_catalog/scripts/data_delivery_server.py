#!/usr/bin/env python3
"""
Data Delivery API Server

This FastAPI server provides endpoints for micro-frontend dashboards to fetch
data for individual reports. It uses the metadata catalog to understand the
hierarchy and MetricFlow to generate SQL queries.

Endpoints:
- GET /api/dashboards - List all dashboards
- GET /api/dashboards/{dashboard_id} - Get dashboard metadata
- GET /api/dashboards/{dashboard_id}/reports - Get all reports for a dashboard
- POST /api/reports/{report_id}/data - Execute a report query and return data

Usage:
    pip install fastapi uvicorn duckdb
    python data_delivery_server.py
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
from pathlib import Path
import json
import duckdb
from datetime import datetime

# Import the metadata catalog
import sys
sys.path.append(str(Path(__file__).parent))
from build_metadata_catalog import MetadataCatalog


app = FastAPI(
    title="BLS Data Delivery API",
    description="Micro-frontend data delivery server for BLS employment dashboards",
    version="1.0.0"
)

# Enable CORS for micro-frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global catalog and database connection
catalog: Optional[MetadataCatalog] = None
db_conn: Optional[duckdb.DuckDBPyConnection] = None


class ReportFilter(BaseModel):
    """Filter criteria for a report query"""
    dimensions: Dict[str, List[str]] = {}
    date_range: Optional[Dict[str, str]] = None
    limit: Optional[int] = None


class ReportDataRequest(BaseModel):
    """Request body for fetching report data"""
    filters: Optional[ReportFilter] = None
    group_by: Optional[List[str]] = None
    metrics: Optional[List[str]] = None


@app.on_event("startup")
async def startup_event():
    """Initialize the metadata catalog and database connection"""
    global catalog, db_conn
    
    # Load the metadata catalog
    project_path = Path(__file__).parent.parent
    try:
        catalog = MetadataCatalog(project_path)
        print(f"✓ Loaded metadata catalog with {len(catalog.dashboards)} dashboards")
    except Exception as e:
        print(f"⚠ Warning: Could not load metadata catalog: {e}")
        print("  Run 'dbt compile' to generate manifest.json")
    
    # Connect to DuckDB
    db_path = project_path / "bls_data.duckdb"
    try:
        db_conn = duckdb.connect(str(db_path), read_only=True)
        print(f"✓ Connected to DuckDB at {db_path}")
    except Exception as e:
        print(f"⚠ Warning: Could not connect to DuckDB: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    """Close database connection"""
    global db_conn
    if db_conn:
        db_conn.close()


@app.get("/")
async def root():
    """API root"""
    return {
        "message": "BLS Data Delivery API",
        "version": "1.0.0",
        "endpoints": {
            "dashboards": "/api/dashboards",
            "reports": "/api/reports",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "catalog_loaded": catalog is not None,
        "database_connected": db_conn is not None,
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/dashboards")
async def list_dashboards():
    """List all available dashboards"""
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    
    dashboards = []
    for dashboard_id, dashboard in catalog.dashboards.items():
        dashboards.append({
            "id": dashboard_id,
            "name": dashboard.name,
            "type": dashboard.type,
            "description": dashboard.description,
            "url": dashboard.url,
            "maturity": dashboard.maturity,
            "report_count": len(dashboard.reports)
        })
    
    return {"dashboards": dashboards, "count": len(dashboards)}


@app.get("/api/dashboards/{dashboard_id}")
async def get_dashboard(dashboard_id: str):
    """Get dashboard metadata including all reports"""
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    
    dashboard = catalog.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail=f"Dashboard {dashboard_id} not found")
    
    # Get report details
    reports = []
    for report_id in dashboard.reports:
        report = catalog.get_report(report_id)
        if report:
            reports.append({
                "id": report_id,
                "name": report.name,
                "description": report.description,
                "visualization_type": report.meta.get("visualization_type"),
                "component": report.meta.get("component")
            })
    
    return {
        "id": dashboard_id,
        "name": dashboard.name,
        "type": dashboard.type,
        "description": dashboard.description,
        "url": dashboard.url,
        "owner": dashboard.owner,
        "maturity": dashboard.maturity,
        "reports": reports,
        "meta": dashboard.meta
    }


@app.get("/api/dashboards/{dashboard_id}/lineage")
async def get_dashboard_lineage(dashboard_id: str):
    """Get complete lineage for a dashboard"""
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    
    try:
        lineage = catalog.get_dashboard_lineage(dashboard_id)
        return lineage
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/api/reports/{report_id}/data")
async def get_report_data(report_id: str, request: ReportDataRequest):
    """
    Execute a report query and return data.
    
    In a real implementation, this would use MetricFlow to generate SQL.
    For this demo, we'll directly query the underlying view.
    """
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    if not db_conn:
        raise HTTPException(status_code=503, detail="Database not connected")
    
    report = catalog.get_report(report_id)
    if not report:
        raise HTTPException(status_code=404, detail=f"Report {report_id} not found")
    
    try:
        # Build a simple SQL query based on the report's semantic model
        # In production, you would use MetricFlow here
        sql = build_report_query(report, request)
        
        # Execute query
        result = db_conn.execute(sql).fetchdf()
        
        # Convert to JSON-serializable format
        data = result.to_dict(orient='records')
        
        return {
            "report_id": report_id,
            "report_name": report.name,
            "data": data,
            "row_count": len(data),
            "sql": sql,  # Include for debugging
            "generated_at": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query execution failed: {str(e)}")


def build_report_query(report: Any, request: ReportDataRequest) -> str:
    """
    Build SQL query for a report.
    
    This is a simplified version. In production, you would use MetricFlow
    to generate the SQL based on the semantic model definition.
    """
    # Get the view/model that the report is based on
    view_name = None
    if report.views:
        view = catalog.get_view(report.views[0])
        if view:
            view_name = f"{view.schema}.{view.name}"
    
    if not view_name:
        raise ValueError(f"Could not determine view for report {report.id}")
    
    # Build SELECT clause
    select_fields = []
    if request.group_by:
        select_fields.extend(request.group_by)
    else:
        # Default group by dimensions from the report
        for dim in report.dimensions[:3]:  # Take first 3 dimensions
            select_fields.append(dim['expr'] if 'expr' in dim else dim['name'])
    
    # Add measures (aggregations)
    if request.metrics:
        for metric in request.metrics:
            # Find the measure definition
            for measure in report.measures:
                if measure['name'] == metric:
                    agg = measure.get('agg', 'sum')
                    expr = measure.get('expr', metric)
                    select_fields.append(f"{agg.upper()}({expr}) as {metric}")
    else:
        # Default to first measure
        if report.measures:
            measure = report.measures[0]
            agg = measure.get('agg', 'sum')
            expr = measure.get('expr', measure['name'])
            select_fields.append(f"{agg.upper()}({expr}) as {measure['name']}")
    
    # Build WHERE clause
    where_clauses = []
    if request.filters:
        if request.filters.dimensions:
            for dim, values in request.filters.dimensions.items():
                if values:
                    value_list = "','".join(values)
                    where_clauses.append(f"{dim} IN ('{value_list}')")
        
        if request.filters.date_range:
            if 'start' in request.filters.date_range:
                where_clauses.append(f"year_month >= '{request.filters.date_range['start']}'")
            if 'end' in request.filters.date_range:
                where_clauses.append(f"year_month <= '{request.filters.date_range['end']}'")
    
    # Build GROUP BY clause
    group_by_fields = request.group_by if request.group_by else [select_fields[0]]
    
    # Assemble query
    sql = f"SELECT {', '.join(select_fields)} FROM {view_name}"
    
    if where_clauses:
        sql += f" WHERE {' AND '.join(where_clauses)}"
    
    sql += f" GROUP BY {', '.join(group_by_fields)}"
    
    # Add LIMIT if specified
    if request.filters and request.filters.limit:
        sql += f" LIMIT {request.filters.limit}"
    
    return sql


@app.get("/api/reports")
async def list_reports():
    """List all available reports"""
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    
    reports = []
    for report_id, report in catalog.reports.items():
        reports.append({
            "id": report_id,
            "name": report.name,
            "description": report.description,
            "dimensions": [d['name'] for d in report.dimensions],
            "measures": [m['name'] for m in report.measures],
            "visualization_type": report.meta.get("visualization_type")
        })
    
    return {"reports": reports, "count": len(reports)}


# Example micro-frontend compatible endpoint
@app.post("/api/dashboards/{dashboard_id}/data")
async def get_all_dashboard_data(
    dashboard_id: str,
    filters: Optional[ReportFilter] = None
):
    """
    Fetch data for all reports in a dashboard.
    This endpoint is optimized for micro-frontends that want to load
    all dashboard data in a single request.
    """
    if not catalog:
        raise HTTPException(status_code=503, detail="Metadata catalog not loaded")
    
    dashboard = catalog.get_dashboard(dashboard_id)
    if not dashboard:
        raise HTTPException(status_code=404, detail=f"Dashboard {dashboard_id} not found")
    
    # Fetch data for each report
    report_data = {}
    for report_id in dashboard.reports:
        try:
            request = ReportDataRequest(filters=filters)
            result = await get_report_data(report_id, request)
            report_data[report_id] = result
        except Exception as e:
            report_data[report_id] = {
                "error": str(e),
                "report_id": report_id
            }
    
    return {
        "dashboard_id": dashboard_id,
        "dashboard_name": dashboard.name,
        "reports": report_data,
        "generated_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    
    print("\n" + "="*60)
    print("BLS Data Delivery API Server")
    print("="*60)
    print("\nStarting server at http://localhost:8000")
    print("API docs available at http://localhost:8000/docs")
    print("\nPress CTRL+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
