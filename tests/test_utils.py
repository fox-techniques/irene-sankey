"""
This module contains unit tests for the `utils` module in the irenesankey package,
specifically testing the `_add_suffix_to_cross_column_duplicates` function.

Tests:
    - test_add_suffix_to_cross_column_duplicates: 
        1. Checks handling of no duplicates. 
        2. Single duplicates across columns.
        3. Multiple duplicates across columns.

    - test_add_suffix_empty_df: 
        Verifies handling of empty DataFrame input.
"""

import pytest
import polars as pl
from irene_sankey.utils.utils import _add_suffix_to_cross_column_duplicates


@pytest.mark.parametrize(
    "df, columns, expected",
    [
        # No duplicates, no changes expected
        (
            pl.DataFrame({"col1": ["A", "B"], "col2": ["C", "D"]}),
            ["col1", "col2"],
            pl.DataFrame({"col1": ["A", "B"], "col2": ["C", "D"]}),
        ),
        # Single duplicate value in a row
        (
            pl.DataFrame({"col1": ["A", "B"], "col2": ["A", "B"]}),
            ["col1", "col2"],
            pl.DataFrame({"col1": ["A", "B"], "col2": ["A-x1", "B-x1"]}),
        ),
    ],
)
def test_add_suffix_to_cross_column_duplicates(df, columns, expected):
    result = _add_suffix_to_cross_column_duplicates(df.clone(), columns)
    assert result.select(columns).equals(expected.select(columns))


def test_add_suffix_empty_df():
    """Test with an empty DataFrame."""
    df = pl.DataFrame({"col1": [], "col2": []})
    result = _add_suffix_to_cross_column_duplicates(df, ["col1", "col2"])
    assert result.is_empty()
