"""Unit tests for load_sample_data.py script."""

from pathlib import Path
from typing import Callable
from unittest.mock import Mock

import pandas as pd
import pytest

from bls_data_catalog.scripts.load_sample_data import (
    download_and_process_bls_employment_data,
)


# Test data fixtures
SAMPLE_CSV_WITH_FOOTNOTES = """year,population,labor_force,population_percent,employed_total,employed_percent,agrictulture_ratio,nonagriculture_ratio,unemployed,unemployed_percent,not_in_labor,footnotes
1941,99900,55910,56.0,50350,50.4,9100,41250,5560,9.9,43990,
1942,98640,56410,57.2,53750,54.5,9250,44500,2660,4.7,42230,
1953,107056,63015,58.9,61179,57.1,6260,54919,1834,2.9,44041,1
1954,108321,63643,58.8,60109,55.5,6205,53904,3532,5.5,44678,"""

SAMPLE_CSV_WITHOUT_FOOTNOTES = """year,population,labor_force,population_percent,employed_total,employed_percent,agrictulture_ratio,nonagriculture_ratio,unemployed,unemployed_percent,not_in_labor
1941,99900,55910,56.0,50350,50.4,9100,41250,5560,9.9,43990
1942,98640,56410,57.2,53750,54.5,9250,44500,2660,4.7,42230
1953,107056,63015,58.9,61179,57.1,6260,54919,1834,2.9,44041
1954,108321,63643,58.8,60109,55.5,6205,53904,3532,5.5,44678"""

# Expected data after processing (footnotes column removed)
EXPECTED_DATA = [
    {
        'year': 1941,
        'population': 99900,
        'labor_force': 55910,
        'population_percent': 56.0,
        'employed_total': 50350,
        'employed_percent': 50.4,
        'agrictulture_ratio': 9100,
        'nonagriculture_ratio': 41250,
        'unemployed': 5560,
        'unemployed_percent': 9.9,
        'not_in_labor': 43990,
    },
    {
        'year': 1942,
        'population': 98640,
        'labor_force': 56410,
        'population_percent': 57.2,
        'employed_total': 53750,
        'employed_percent': 54.5,
        'agrictulture_ratio': 9250,
        'nonagriculture_ratio': 44500,
        'unemployed': 2660,
        'unemployed_percent': 4.7,
        'not_in_labor': 42230,
    },
    {
        'year': 1953,
        'population': 107056,
        'labor_force': 63015,
        'population_percent': 58.9,
        'employed_total': 61179,
        'employed_percent': 57.1,
        'agrictulture_ratio': 6260,
        'nonagriculture_ratio': 54919,
        'unemployed': 1834,
        'unemployed_percent': 2.9,
        'not_in_labor': 44041,
    },
    {
        'year': 1954,
        'population': 108321,
        'labor_force': 63643,
        'population_percent': 58.8,
        'employed_total': 60109,
        'employed_percent': 55.5,
        'agrictulture_ratio': 6205,
        'nonagriculture_ratio': 53904,
        'unemployed': 3532,
        'unemployed_percent': 5.5,
        'not_in_labor': 44678,
    },
]


@pytest.fixture
def expected_dataframe() -> pd.DataFrame:
    """
    Create the expected DataFrame after processing.

    Returns:
        Expected pandas DataFrame with cleaned data
    """
    return pd.DataFrame(EXPECTED_DATA)


@pytest.fixture
def mock_fetch_csv() -> Callable[[str], str]:
    """
    Create a mock fetch function for testing.

    Returns:
        Mock function that returns sample CSV data
    """
    mock = Mock(spec=lambda url: str)
    mock.return_value = SAMPLE_CSV_WITH_FOOTNOTES
    return mock


@pytest.fixture
def temp_output_path(tmp_path: Path) -> Path:
    """
    Create a temporary output path for testing.

    Args:
        tmp_path: pytest's temporary directory fixture

    Returns:
        Path to temporary output file
    """
    return tmp_path / "output" / "test_employment.csv"


class TestDownloadAndProcessBlsEmploymentData:
    """Tests for download_and_process_bls_employment_data function."""

    def test_calls_fetch_function_with_url(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that fetch function is called with the correct URL."""
        test_url = "https://example.com/data.csv"

        download_and_process_bls_employment_data(test_url, temp_output_path, mock_fetch_csv)

        mock_fetch_csv.assert_called_once_with(test_url)

    def test_returns_dataframe(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that function returns a pandas DataFrame."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert isinstance(result, pd.DataFrame)

    def test_returns_dataframe_with_correct_shape(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that returned DataFrame has correct number of rows and columns."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert len(result) == 4  # 4 data rows
        assert len(result.columns) == 11  # 11 columns (footnotes removed)

    def test_removes_footnotes_column(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that footnotes column is removed from returned DataFrame."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert 'footnotes' not in result.columns

    def test_returns_expected_dataframe(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
        expected_dataframe: pd.DataFrame,
    ) -> None:
        """Test that function returns the expected DataFrame with correct data."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        # Compare entire DataFrames
        pd.testing.assert_frame_equal(result, expected_dataframe)

    def test_returns_correct_columns(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that DataFrame has the expected column names."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        expected_columns = [
            'year',
            'population',
            'labor_force',
            'population_percent',
            'employed_total',
            'employed_percent',
            'agrictulture_ratio',
            'nonagriculture_ratio',
            'unemployed',
            'unemployed_percent',
            'not_in_labor',
        ]

        assert list(result.columns) == expected_columns

    def test_saves_file_to_output_path(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that data is saved to the specified output path."""
        download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert temp_output_path.exists()

    def test_saved_file_matches_returned_dataframe(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
        expected_dataframe: pd.DataFrame,
    ) -> None:
        """Test that saved file contents match the returned DataFrame."""
        result = download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        # Read the saved file
        saved_df = pd.read_csv(temp_output_path)

        # Compare all three: result, saved file, and expected
        pd.testing.assert_frame_equal(result, saved_df)
        pd.testing.assert_frame_equal(saved_df, expected_dataframe)

    def test_creates_parent_directory_if_missing(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that parent directory is created if it doesn't exist."""
        # Ensure parent doesn't exist
        assert not temp_output_path.parent.exists()

        download_and_process_bls_employment_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert temp_output_path.parent.exists()
        assert temp_output_path.exists()
