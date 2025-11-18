#!/usr/bin/env python3
"""
Fetch real BLS LAUS (Local Area Unemployment Statistics) data and load into DuckDB.
Retrieves employment and unemployment data for all 50 states from the BLS Public Data API.
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

try:
    import duckdb
except ImportError:
    print("Error: 'duckdb' library not found. Install with: pip install duckdb")
    sys.exit(1)

# BLS API Configuration
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
MAX_SERIES_PER_REQUEST = 50  # BLS API limit
MAX_YEARS_UNAUTHENTICATED = 10  # BLS API limit without API key

# State FIPS codes (50 states + DC)
STATE_FIPS = [
    '01', '02', '04', '05', '06', '08', '09', '10', '11', '12',
    '13', '15', '16', '17', '18', '19', '20', '21', '22', '23',
    '24', '25', '26', '27', '28', '29', '30', '31', '32', '33',
    '34', '35', '36', '37', '38', '39', '40', '41', '42', '44',
    '45', '46', '47', '48', '49', '50', '51', '53', '54', '55', '56'
]

# BLS LAUS Series ID patterns
# Format: LAUST{state_fips}0000000000{measure}
# Measure 03 = Employment Level (in thousands)
# Measure 04 = Unemployment Rate (percent)
# Measure 05 = Labor Force (in thousands)
# Measure 06 = Unemployed (in thousands)
EMPLOYMENT_MEASURE = '03'
UNEMPLOYMENT_MEASURE = '04'
LABOR_FORCE_MEASURE = '05'
UNEMPLOYED_MEASURE = '06'


def build_series_ids(measure: str) -> List[str]:
    """Build BLS LAUS series IDs for all states."""
    return [f'LAUST{fips}0000000000{measure}' for fips in STATE_FIPS]


def fetch_bls_data(series_ids: List[str], start_year: int, end_year: int) -> Dict[str, Any]:
    """
    Fetch data from BLS API for given series IDs and year range.

    Args:
        series_ids: List of BLS series IDs to fetch
        start_year: Starting year for data
        end_year: Ending year for data

    Returns:
        Dictionary containing API response data
    """
    payload = {
        "seriesid": series_ids,
        "startyear": str(start_year),
        "endyear": str(end_year)
    }

    headers = {'Content-Type': 'application/json'}

    print(f"  Fetching {len(series_ids)} series from {start_year} to {end_year}...")

    try:
        response = requests.post(BLS_API_URL, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        if data.get('status') != 'REQUEST_SUCCEEDED':
            error_msg = data.get('message', ['Unknown error'])[0]
            raise Exception(f"BLS API error: {error_msg}")

        return data

    except requests.exceptions.RequestException as e:
        raise Exception(f"Failed to fetch BLS data: {e}")


def parse_employment_data(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse employment data from BLS API response.

    Returns:
        List of employment records with columns: state_fips, year_month, employment_level, series_id
    """
    records = []

    for series in api_response.get('Results', {}).get('series', []):
        series_id = series['seriesID']
        # Extract state FIPS from series ID (positions 5-6)
        state_fips = series_id[5:7]

        for data_point in series.get('data', []):
            year = data_point['year']
            # Period format: M01, M02, ..., M12
            period = data_point['period']

            # Skip annual averages (M13)
            if not period.startswith('M') or period == 'M13':
                continue

            month = period[1:3]
            year_month = f"{year}-{month}-01"

            # Employment level is in thousands
            try:
                employment_level = int(float(data_point['value']))
            except (ValueError, TypeError):
                print(f"  Warning: Invalid employment value for {series_id} {year_month}: {data_point.get('value')}")
                continue

            records.append({
                'state_fips': state_fips,
                'year_month': year_month,
                'employment_level': employment_level,
                'series_id': series_id
            })

    return records


def parse_unemployment_data(api_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse unemployment data from BLS API response.

    Note: BLS LAUS measure 04 only provides unemployment rate.
    We need to fetch additional measures for labor force (05) and unemployed count (06).
    For now, we'll calculate approximate values based on the rate.

    Returns:
        List of unemployment records with columns: state_fips, year_month, unemployment_rate,
        labor_force, unemployed, series_id
    """
    records = []

    for series in api_response.get('Results', {}).get('series', []):
        series_id = series['seriesID']
        state_fips = series_id[5:7]

        for data_point in series.get('data', []):
            year = data_point['year']
            period = data_point['period']

            # Skip annual averages
            if not period.startswith('M') or period == 'M13':
                continue

            month = period[1:3]
            year_month = f"{year}-{month}-01"

            try:
                unemployment_rate = float(data_point['value'])
            except (ValueError, TypeError):
                print(f"  Warning: Invalid unemployment rate for {series_id} {year_month}: {data_point.get('value')}")
                continue

            # Note: We'll need to fetch labor force and unemployed counts separately
            # For now, set to 0 - will be filled in by fetching additional measures
            records.append({
                'state_fips': state_fips,
                'year_month': year_month,
                'unemployment_rate': round(unemployment_rate, 1),
                'labor_force': 0,  # Placeholder
                'unemployed': 0,   # Placeholder
                'series_id': series_id
            })

    return records


def fetch_labor_force_data(start_year: int, end_year: int) -> Dict[str, Dict[str, int]]:
    """
    Fetch labor force (measure 05) and unemployed (measure 06) data from BLS API.

    Returns:
        Dictionary mapping (state_fips, year_month) to (labor_force, unemployed)
    """
    print("\nFetching labor force and unemployed counts...")

    # Fetch labor force (measure 05)
    labor_force_ids = build_series_ids(LABOR_FORCE_MEASURE)

    # Batch requests
    labor_force_data = {}
    for i in range(0, len(labor_force_ids), MAX_SERIES_PER_REQUEST):
        batch = labor_force_ids[i:i + MAX_SERIES_PER_REQUEST]
        response = fetch_bls_data(batch, start_year, end_year)

        for series in response.get('Results', {}).get('series', []):
            series_id = series['seriesID']
            state_fips = series_id[5:7]

            for data_point in series.get('data', []):
                year = data_point['year']
                period = data_point['period']

                if not period.startswith('M') or period == 'M13':
                    continue

                month = period[1:3]
                year_month = f"{year}-{month}-01"

                try:
                    value = int(float(data_point['value']))
                    key = (state_fips, year_month)
                    if key not in labor_force_data:
                        labor_force_data[key] = {'labor_force': 0, 'unemployed': 0}
                    labor_force_data[key]['labor_force'] = value
                except (ValueError, TypeError):
                    continue

    # Fetch unemployed (measure 06)
    print("\nFetching unemployed counts...")
    unemployed_ids = build_series_ids(UNEMPLOYED_MEASURE)

    for i in range(0, len(unemployed_ids), MAX_SERIES_PER_REQUEST):
        batch = unemployed_ids[i:i + MAX_SERIES_PER_REQUEST]
        response = fetch_bls_data(batch, start_year, end_year)

        for series in response.get('Results', {}).get('series', []):
            series_id = series['seriesID']
            state_fips = series_id[5:7]

            for data_point in series.get('data', []):
                year = data_point['year']
                period = data_point['period']

                if not period.startswith('M') or period == 'M13':
                    continue

                month = period[1:3]
                year_month = f"{year}-{month}-01"

                try:
                    value = int(float(data_point['value']))
                    key = (state_fips, year_month)
                    if key not in labor_force_data:
                        labor_force_data[key] = {'labor_force': 0, 'unemployed': 0}
                    labor_force_data[key]['unemployed'] = value
                except (ValueError, TypeError):
                    continue

    return labor_force_data


def enrich_unemployment_data(records: List[Dict[str, Any]], labor_force_data: Dict) -> List[Dict[str, Any]]:
    """Add labor force and unemployed counts to unemployment records."""
    for record in records:
        key = (record['state_fips'], record['year_month'])
        if key in labor_force_data:
            record['labor_force'] = labor_force_data[key]['labor_force']
            record['unemployed'] = labor_force_data[key]['unemployed']

    return records


def write_to_duckdb(employment_data: List[Dict], unemployment_data: List[Dict], output_path: Path):
    """
    Write employment and unemployment data to DuckDB file.

    Args:
        employment_data: List of employment records
        unemployment_data: List of unemployment records
        output_path: Path to DuckDB file
    """
    print(f"\nWriting data to DuckDB: {output_path}")

    # Connect to DuckDB (creates file if doesn't exist)
    conn = duckdb.connect(str(output_path))

    try:
        # Create raw schema
        conn.execute("CREATE SCHEMA IF NOT EXISTS raw")

        # Drop existing tables if they exist
        conn.execute("DROP TABLE IF EXISTS raw.employment_monthly")
        conn.execute("DROP TABLE IF EXISTS raw.unemployment_monthly")

        # Create and populate employment table
        print("  Creating raw.employment_monthly table...")
        conn.execute("""
            CREATE TABLE raw.employment_monthly (
                state_fips VARCHAR,
                year_month DATE,
                employment_level INTEGER,
                series_id VARCHAR
            )
        """)

        conn.executemany(
            "INSERT INTO raw.employment_monthly VALUES (?, ?, ?, ?)",
            [(r['state_fips'], r['year_month'], r['employment_level'], r['series_id'])
             for r in employment_data]
        )

        emp_count = conn.execute("SELECT COUNT(*) FROM raw.employment_monthly").fetchone()[0]
        print(f"    ✓ Inserted {emp_count} employment records")

        # Create and populate unemployment table
        print("  Creating raw.unemployment_monthly table...")
        conn.execute("""
            CREATE TABLE raw.unemployment_monthly (
                state_fips VARCHAR,
                year_month DATE,
                unemployment_rate DOUBLE,
                labor_force INTEGER,
                unemployed INTEGER,
                series_id VARCHAR
            )
        """)

        conn.executemany(
            "INSERT INTO raw.unemployment_monthly VALUES (?, ?, ?, ?, ?, ?)",
            [(r['state_fips'], r['year_month'], r['unemployment_rate'],
              r['labor_force'], r['unemployed'], r['series_id'])
             for r in unemployment_data]
        )

        unemp_count = conn.execute("SELECT COUNT(*) FROM raw.unemployment_monthly").fetchone()[0]
        print(f"    ✓ Inserted {unemp_count} unemployment records")

        # Copy states.csv to raw.states table if it exists
        states_csv = output_path.parent / 'states.csv'
        if states_csv.exists():
            print("  Creating raw.states table from states.csv...")
            conn.execute("DROP TABLE IF EXISTS raw.states")
            conn.execute(f"""
                CREATE TABLE raw.states AS
                SELECT * FROM read_csv_auto('{states_csv}')
            """)
            states_count = conn.execute("SELECT COUNT(*) FROM raw.states").fetchone()[0]
            print(f"    ✓ Loaded {states_count} state records")

        conn.commit()

    finally:
        conn.close()


def main():
    """Main execution function."""
    print("=" * 70)
    print("BLS LAUS Data Loader")
    print("=" * 70)

    # Determine date range (last 3 years)
    current_year = datetime.now().year
    end_year = current_year
    start_year = end_year - 2  # 3 years of data

    print(f"\nFetching data for {start_year}-{end_year} (3 years)")
    print(f"Data source: BLS LAUS (Local Area Unemployment Statistics)")
    print(f"Coverage: All 50 states + DC ({len(STATE_FIPS)} states)")

    # Prepare output directory and file
    # Write to the main project directory where dbt expects it (profiles.yml: path: './bls_data.duckdb')
    project_dir = Path(__file__).parent.parent
    output_db = project_dir / 'bls_data.duckdb'

    # Also ensure data directory exists for states.csv reference
    data_dir = project_dir / 'data'
    data_dir.mkdir(exist_ok=True)

    try:
        # Fetch employment data
        print("\n" + "=" * 70)
        print("Fetching Employment Data (Measure 03)")
        print("=" * 70)
        employment_series = build_series_ids(EMPLOYMENT_MEASURE)

        employment_records = []
        # Batch requests to stay within API limits
        for i in range(0, len(employment_series), MAX_SERIES_PER_REQUEST):
            batch = employment_series[i:i + MAX_SERIES_PER_REQUEST]
            response = fetch_bls_data(batch, start_year, end_year)
            employment_records.extend(parse_employment_data(response))

        print(f"  ✓ Retrieved {len(employment_records)} employment records")

        # Fetch unemployment data
        print("\n" + "=" * 70)
        print("Fetching Unemployment Data (Measure 04)")
        print("=" * 70)
        unemployment_series = build_series_ids(UNEMPLOYMENT_MEASURE)

        unemployment_records = []
        for i in range(0, len(unemployment_series), MAX_SERIES_PER_REQUEST):
            batch = unemployment_series[i:i + MAX_SERIES_PER_REQUEST]
            response = fetch_bls_data(batch, start_year, end_year)
            unemployment_records.extend(parse_unemployment_data(response))

        print(f"  ✓ Retrieved {len(unemployment_records)} unemployment records")

        # Fetch labor force and unemployed counts
        print("\n" + "=" * 70)
        print("Fetching Labor Force & Unemployed Counts (Measures 05, 06)")
        print("=" * 70)
        labor_force_data = fetch_labor_force_data(start_year, end_year)
        unemployment_records = enrich_unemployment_data(unemployment_records, labor_force_data)
        print(f"  ✓ Enriched unemployment records with labor force data")

        # Write to DuckDB
        print("\n" + "=" * 70)
        print("Writing to DuckDB")
        print("=" * 70)
        write_to_duckdb(employment_records, unemployment_records, output_db)

        print("\n" + "=" * 70)
        print("✓ SUCCESS")
        print("=" * 70)
        print(f"Data loaded to: {output_db}")
        print(f"  - raw.employment_monthly: {len(employment_records)} records")
        print(f"  - raw.unemployment_monthly: {len(unemployment_records)} records")
        print("\nNext steps:")
        print("  1. Run 'dbt run' to build analytics views")
        print("  2. Run 'dbt docs generate' to update documentation")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
