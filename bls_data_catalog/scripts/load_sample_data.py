#!/usr/bin/env python3
"""
Download US employment data from the employment-us dataset and save to seed folder.

This script downloads historical US employment statistics from the GitHub repository
datasets/employment-us and saves it as a cleaned CSV file in the dbt seeds directory.

Source: https://github.com/datasets/employment-us
"""

import sys
from io import StringIO
from pathlib import Path
from typing import Callable, Final

try:
    import pandas as pd
except ImportError:
    print("Error: 'pandas' library not found. Install with: pip install pandas")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)

# Data source configuration
DATA_URL: Final[str] = "https://github.com/datasets/employment-us/raw/refs/heads/main/data/aat1.csv"
OUTPUT_FILENAME: Final[str] = "us_employment.csv"
REQUEST_TIMEOUT: Final[int] = 30

# Columns to exclude from the final dataset
EXCLUDED_COLUMNS: Final[list[str]] = ['footnotes']


def fetch_csv_data(url: str) -> str:
    """
    Fetch CSV data from a URL.

    Args:
        url: URL to the raw CSV file

    Returns:
        Raw CSV content as string

    Raises:
        requests.exceptions.RequestException: If download fails
    """
    response = requests.get(url, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.text


def clean_employment_data(raw_csv: str) -> pd.DataFrame:
    """
    Clean and process employment data CSV.

    Removes the 'footnotes' column which has inconsistent data
    (some rows have values, some are empty).

    Args:
        raw_csv: Raw CSV content as string

    Returns:
        Cleaned pandas DataFrame
    """
    # Read CSV into DataFrame
    df = pd.read_csv(StringIO(raw_csv))

    # Drop excluded columns
    columns_to_drop = [col for col in EXCLUDED_COLUMNS if col in df.columns]
    if columns_to_drop:
        df = df.drop(columns=columns_to_drop)

    return df


def save_dataframe(df: pd.DataFrame, output_path: Path) -> None:
    """
    Save DataFrame to CSV file.

    Args:
        df: DataFrame to save
        output_path: Path where the CSV should be saved
    """
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save to CSV
    df.to_csv(output_path, index=False)


def download_and_process_data(
    url: str,
    output_path: Path,
    fetch_func: Callable[[str], str] = fetch_csv_data,
) -> int:
    """
    Download employment data, clean it, and save to file.

    Args:
        url: URL to the raw CSV file
        output_path: Path where the CSV should be saved
        fetch_func: Function to fetch CSV data from URL (default: fetch_csv_data)

    Returns:
        Number of records processed

    Raises:
        requests.exceptions.RequestException: If download fails
        Exception: If data processing fails
    """
    print(f"Downloading data from: {url}")

    # Fetch raw CSV data
    raw_csv = fetch_func(url)

    # Clean the data
    print("Cleaning data...")
    df = clean_employment_data(raw_csv)

    # Save to file
    save_dataframe(df, output_path)

    return len(df)


def main() -> None:
    """Main execution function."""
    print("=" * 70)
    print("US Employment Data Loader")
    print("=" * 70)
    print(f"\nData source: employment-us dataset")
    print(f"URL: {DATA_URL}")

    # Determine output path (data directory is the seed folder)
    project_dir = Path(__file__).parent.parent
    data_dir = project_dir / 'data'
    output_file = data_dir / OUTPUT_FILENAME

    try:
        record_count = download_and_process_data(DATA_URL, output_file)

        print(f"✓ Successfully processed {record_count:,} records")
        print(f"✓ Saved to: {output_file}")

        print("\n" + "=" * 70)
        print("✓ SUCCESS")
        print("=" * 70)
        print("\nNext steps:")
        print("  1. Run 'dbt seed --profiles-dir .' to load CSV into DuckDB")
        print("  2. Run 'dbt run --profiles-dir .' to build analytics views")
        print("  3. Run 'dbt docs generate --profiles-dir .' to update documentation")

    except requests.exceptions.RequestException as e:
        print(f"\n✗ ERROR: Failed to download data: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
