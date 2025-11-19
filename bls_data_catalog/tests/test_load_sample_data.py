"""Unit tests for load_sample_data.py script."""

import tempfile
from pathlib import Path
from typing import Callable
from unittest.mock import Mock

import pandas as pd
import pytest

from bls_data_catalog.scripts.load_sample_data import (
    clean_employment_data,
    download_and_process_data,
    save_dataframe,
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


class TestCleanEmploymentData:
    """Tests for clean_employment_data function."""

    def test_removes_footnotes_column(self) -> None:
        """Test that footnotes column is removed from the data."""
        result = clean_employment_data(SAMPLE_CSV_WITH_FOOTNOTES)

        assert 'footnotes' not in result.columns
        assert len(result.columns) == 11

    def test_preserves_data_integrity(self) -> None:
        """Test that data values are preserved after cleaning."""
        result = clean_employment_data(SAMPLE_CSV_WITH_FOOTNOTES)

        assert len(result) == 4
        assert result.iloc[0]['year'] == 1941
        assert result.iloc[0]['population'] == 99900
        assert result.iloc[0]['labor_force'] == 55910

    def test_handles_csv_without_footnotes(self) -> None:
        """Test that function works with CSV that doesn't have footnotes column."""
        result = clean_employment_data(SAMPLE_CSV_WITHOUT_FOOTNOTES)

        assert len(result.columns) == 11
        assert len(result) == 4

    def test_column_names_are_correct(self) -> None:
        """Test that expected columns are present."""
        result = clean_employment_data(SAMPLE_CSV_WITH_FOOTNOTES)

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

    def test_returns_dataframe(self) -> None:
        """Test that function returns a pandas DataFrame."""
        result = clean_employment_data(SAMPLE_CSV_WITH_FOOTNOTES)

        assert isinstance(result, pd.DataFrame)


class TestSaveDataframe:
    """Tests for save_dataframe function."""

    def test_creates_output_directory(self, temp_output_path: Path) -> None:
        """Test that parent directory is created if it doesn't exist."""
        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})

        save_dataframe(df, temp_output_path)

        assert temp_output_path.parent.exists()
        assert temp_output_path.exists()

    def test_saves_csv_correctly(self, temp_output_path: Path) -> None:
        """Test that DataFrame is saved correctly to CSV."""
        df = pd.DataFrame({'year': [1941, 1942], 'population': [99900, 98640]})

        save_dataframe(df, temp_output_path)

        # Read back the CSV and verify
        result = pd.read_csv(temp_output_path)
        pd.testing.assert_frame_equal(result, df)

    def test_saves_without_index(self, temp_output_path: Path) -> None:
        """Test that CSV is saved without index column."""
        df = pd.DataFrame({'year': [1941, 1942], 'population': [99900, 98640]})

        save_dataframe(df, temp_output_path)

        # Read the file as text and check first line
        content = temp_output_path.read_text()
        first_line = content.split('\n')[0]

        # Should not have an unnamed index column
        assert first_line == 'year,population'


class TestDownloadAndProcessData:
    """Tests for download_and_process_data function."""

    def test_calls_fetch_function_with_url(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that fetch function is called with the correct URL."""
        test_url = "https://example.com/data.csv"

        download_and_process_data(test_url, temp_output_path, mock_fetch_csv)

        mock_fetch_csv.assert_called_once_with(test_url)

    def test_returns_correct_record_count(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that function returns the correct number of records processed."""
        result = download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert result == 4

    def test_saves_cleaned_data_to_file(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that cleaned data is saved to the output file."""
        download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        assert temp_output_path.exists()

        # Verify the saved data
        df = pd.read_csv(temp_output_path)
        assert len(df) == 4
        assert 'footnotes' not in df.columns
        assert len(df.columns) == 11

    def test_data_integrity_in_saved_file(
        self,
        mock_fetch_csv: Mock,
        temp_output_path: Path,
    ) -> None:
        """Test that data values are preserved in the saved file."""
        download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch_csv,
        )

        df = pd.read_csv(temp_output_path)

        # Check first row
        assert df.iloc[0]['year'] == 1941
        assert df.iloc[0]['population'] == 99900
        assert df.iloc[0]['unemployed'] == 5560

    def test_handles_different_fetch_functions(
        self,
        temp_output_path: Path,
    ) -> None:
        """Test that function works with different fetch function implementations."""
        # Custom fetch function
        def custom_fetch(url: str) -> str:
            return SAMPLE_CSV_WITHOUT_FOOTNOTES

        result = download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            custom_fetch,
        )

        assert result == 4
        assert temp_output_path.exists()

    def test_fetch_function_can_be_injected(
        self,
        temp_output_path: Path,
    ) -> None:
        """Test that fetch function can be injected as a dependency."""
        # Create a custom mock fetch function
        custom_fetch = Mock(return_value=SAMPLE_CSV_WITH_FOOTNOTES)

        # Call with custom fetch function
        result = download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            fetch_func=custom_fetch,
        )

        # Verify the custom fetch was called
        assert result == 4
        custom_fetch.assert_called_once_with("https://example.com/data.csv")


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_end_to_end_workflow(
        self,
        temp_output_path: Path,
    ) -> None:
        """Test the complete workflow from fetch to save."""
        # Create a mock fetch function
        def mock_fetch(url: str) -> str:
            return SAMPLE_CSV_WITH_FOOTNOTES

        # Run the complete workflow
        record_count = download_and_process_data(
            "https://example.com/data.csv",
            temp_output_path,
            mock_fetch,
        )

        # Verify results
        assert record_count == 4
        assert temp_output_path.exists()

        # Load and verify the saved data
        df = pd.read_csv(temp_output_path)
        assert len(df) == 4
        assert list(df.columns) == [
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

        # Verify data values
        assert df.iloc[0]['year'] == 1941
        assert df.iloc[2]['year'] == 1953
        assert df.iloc[2]['unemployed'] == 1834
