#!/usr/bin/env python3
"""
Metadata Catalog Builder for BLS Employment Data

This script parses dbt's compiled artifacts (manifest.json, semantic_manifest.json)
and builds a hierarchical metadata catalog with four layers:
1. Tables (sources)
2. Views (models)
3. Reports (semantic models)
4. Dashboards (exposures)

It demonstrates how to traverse the lineage and query the hierarchy.
"""

import json
from pathlib import Path
from typing import Dict, List, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class Table:
    """Base layer: dbt source"""
    id: str
    name: str
    schema: str
    database: str
    source_name: str
    description: str
    meta: Dict[str, Any]


@dataclass
class View:
    """Second layer: dbt model"""
    id: str
    name: str
    schema: str
    database: str
    materialization: str
    description: str
    tables: List[str]  # Source dependencies
    meta: Dict[str, Any]


@dataclass
class Report:
    """Third layer: dbt semantic model"""
    id: str
    name: str
    description: str
    model: str  # View dependency
    entities: List[Dict[str, Any]]
    dimensions: List[Dict[str, Any]]
    measures: List[Dict[str, Any]]
    views: List[str]  # View dependencies (from model reference)
    meta: Dict[str, Any]


@dataclass
class Dashboard:
    """Top layer: dbt exposure"""
    id: str
    name: str
    type: str
    description: str
    url: str
    owner: Dict[str, str]
    maturity: str
    reports: List[str]  # Report dependencies
    depends_on: List[str]  # Model dependencies
    meta: Dict[str, Any]


class MetadataCatalog:
    """
    Metadata catalog that understands the hierarchical relationships
    between Tables -> Views -> Reports -> Dashboards
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.manifest = self._load_manifest()
        self.semantic_manifest = self._load_semantic_manifest()
        
        # Storage for each layer
        self.tables: Dict[str, Table] = {}
        self.views: Dict[str, View] = {}
        self.reports: Dict[str, Report] = {}
        self.dashboards: Dict[str, Dashboard] = {}
        
        # Build the catalog
        self._build_catalog()
    
    def _load_manifest(self) -> Dict:
        """Load dbt's manifest.json"""
        manifest_path = self.project_path / "target/manifest.json"
        if not manifest_path.exists():
            raise FileNotFoundError(
                f"manifest.json not found at {manifest_path}. "
                "Run 'dbt compile' first."
            )
        with open(manifest_path) as f:
            return json.load(f)
    
    def _load_semantic_manifest(self) -> Dict:
        """Load semantic_manifest.json for MetricFlow"""
        semantic_path = self.project_path / "target/semantic_manifest.json"
        if not semantic_path.exists():
            # Semantic manifest may not exist if no semantic models defined
            return {"semantic_models": {}}
        with open(semantic_path) as f:
            return json.load(f)
    
    def _build_catalog(self):
        """Build the complete catalog from dbt artifacts"""
        self._parse_sources()
        self._parse_models()
        self._parse_semantic_models()
        self._parse_exposures()
    
    def _parse_sources(self):
        """Parse dbt sources into Tables"""
        for node_id, node in self.manifest.get('sources', {}).items():
            table = Table(
                id=node_id,
                name=node['name'],
                schema=node['schema'],
                database=node['database'],
                source_name=node['source_name'],
                description=node.get('description', ''),
                meta=node.get('meta', {})
            )
            self.tables[node_id] = table
    
    def _parse_models(self):
        """Parse dbt models into Views"""
        for node_id, node in self.manifest.get('nodes', {}).items():
            if node['resource_type'] == 'model':
                # Get upstream table dependencies
                depends_on = node.get('depends_on', {}).get('nodes', [])
                tables = [dep for dep in depends_on if dep.startswith('source.')]
                
                view = View(
                    id=node_id,
                    name=node['name'],
                    schema=node['schema'],
                    database=node['database'],
                    materialization=node.get('config', {}).get('materialized', 'view'),
                    description=node.get('description', ''),
                    tables=tables,
                    meta=node.get('meta', {})
                )
                self.views[node_id] = view
    
    def _parse_semantic_models(self):
        """Parse semantic models into Reports"""
        # Note: The structure of semantic_manifest.json varies by dbt version
        # This is a simplified parser
        semantic_models = self.semantic_manifest.get('semantic_models', {})
        
        if not semantic_models:
            print("Warning: No semantic models found in semantic_manifest.json")
            return
        
        for sm_id, sm in semantic_models.items():
            # Get the model reference
            model_ref = sm.get('model', '')
            
            # Convert ref('model_name') to node_id
            views = []
            if model_ref:
                # Try to find matching model
                for node_id, view in self.views.items():
                    if view.name in model_ref or node_id in model_ref:
                        views.append(node_id)
            
            report = Report(
                id=sm_id,
                name=sm.get('name', sm_id),
                description=sm.get('description', ''),
                model=model_ref,
                entities=sm.get('entities', []),
                dimensions=sm.get('dimensions', []),
                measures=sm.get('measures', []),
                views=views,
                meta=sm.get('meta', {})
            )
            self.reports[sm_id] = report
    
    def _parse_exposures(self):
        """Parse dbt exposures into Dashboards"""
        for node_id, node in self.manifest.get('exposures', {}).items():
            # Get model dependencies
            depends_on = node.get('depends_on', {}).get('nodes', [])
            
            # Get report dependencies from meta
            report_ids = node.get('meta', {}).get('reports', [])
            
            dashboard = Dashboard(
                id=node_id,
                name=node['name'],
                type=node.get('type', 'dashboard'),
                description=node.get('description', ''),
                url=node.get('url', ''),
                owner=node.get('owner', {}),
                maturity=node.get('maturity', 'low'),
                reports=report_ids,
                depends_on=depends_on,
                meta=node.get('meta', {})
            )
            self.dashboards[node_id] = dashboard
    
    # Query methods
    
    def get_dashboard(self, dashboard_id: str) -> Dashboard:
        """Get dashboard by ID"""
        return self.dashboards.get(dashboard_id)
    
    def get_report(self, report_id: str) -> Report:
        """Get report by ID"""
        return self.reports.get(report_id)
    
    def get_view(self, view_id: str) -> View:
        """Get view by ID"""
        return self.views.get(view_id)
    
    def get_table(self, table_id: str) -> Table:
        """Get table by ID"""
        return self.tables.get(table_id)
    
    def get_dashboard_lineage(self, dashboard_id: str) -> Dict[str, Any]:
        """
        Get complete lineage for a dashboard:
        Dashboard -> Reports -> Views -> Tables
        """
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            raise ValueError(f"Dashboard {dashboard_id} not found")
        
        lineage = {
            'dashboard': asdict(dashboard),
            'reports': {},
            'views': {},
            'tables': {}
        }
        
        # For each report in the dashboard
        for report_id in dashboard.reports:
            report = self.reports.get(report_id)
            if report:
                lineage['reports'][report_id] = asdict(report)
                
                # For each view in the report
                for view_id in report.views:
                    view = self.views.get(view_id)
                    if view:
                        lineage['views'][view_id] = asdict(view)
                        
                        # For each table in the view
                        for table_id in view.tables:
                            table = self.tables.get(table_id)
                            if table:
                                lineage['tables'][table_id] = asdict(table)
        
        return lineage
    
    def get_reports_for_dashboard(self, dashboard_id: str) -> List[Report]:
        """Get all reports that belong to a dashboard"""
        dashboard = self.dashboards.get(dashboard_id)
        if not dashboard:
            return []
        
        return [
            self.reports[rid] 
            for rid in dashboard.reports 
            if rid in self.reports
        ]
    
    def get_views_for_report(self, report_id: str) -> List[View]:
        """Get all views that a report depends on"""
        report = self.reports.get(report_id)
        if not report:
            return []
        
        return [
            self.views[vid] 
            for vid in report.views 
            if vid in self.views
        ]
    
    def export_catalog(self, output_path: str):
        """Export the entire catalog as JSON"""
        catalog = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'project_path': str(self.project_path),
                'dbt_version': self.manifest.get('metadata', {}).get('dbt_version')
            },
            'tables': {k: asdict(v) for k, v in self.tables.items()},
            'views': {k: asdict(v) for k, v in self.views.items()},
            'reports': {k: asdict(v) for k, v in self.reports.items()},
            'dashboards': {k: asdict(v) for k, v in self.dashboards.items()}
        }
        
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output, 'w') as f:
            json.dump(catalog, f, indent=2)
        
        print(f"✓ Catalog exported to {output}")
    
    def print_summary(self):
        """Print a summary of the catalog"""
        print("\n" + "="*60)
        print("BLS Data Catalog Summary")
        print("="*60)
        print(f"\nTables (Sources):     {len(self.tables)}")
        print(f"Views (Models):       {len(self.views)}")
        print(f"Reports (Sem Models): {len(self.reports)}")
        print(f"Dashboards (Exp):     {len(self.dashboards)}")
        
        print("\n" + "-"*60)
        print("Dashboards:")
        print("-"*60)
        for dashboard_id, dashboard in self.dashboards.items():
            print(f"\n📊 {dashboard.name}")
            print(f"   ID: {dashboard_id}")
            print(f"   Reports: {len(dashboard.reports)}")
            print(f"   URL: {dashboard.url}")
            
            for report_id in dashboard.reports:
                if report_id in self.reports:
                    report = self.reports[report_id]
                    print(f"     → {report.name}")
        print("\n" + "="*60)


def main():
    """Demo usage of the metadata catalog"""
    import sys
    
    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = Path(__file__).parent.parent
    
    print(f"Building metadata catalog from: {project_path}")
    
    # Build the catalog
    catalog = MetadataCatalog(project_path)
    
    # Print summary
    catalog.print_summary()
    
    # Export to JSON
    catalog.export_catalog(f"{project_path}/target/metadata_catalog.json")
    
    # Example: Get lineage for first dashboard
    if catalog.dashboards:
        first_dashboard_id = list(catalog.dashboards.keys())[0]
        print(f"\n\nExample: Lineage for {first_dashboard_id}")
        print("-"*60)
        
        lineage = catalog.get_dashboard_lineage(first_dashboard_id)
        print(json.dumps(lineage, indent=2))


if __name__ == '__main__':
    main()
