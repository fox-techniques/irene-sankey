"""
This module contains internal utility functions for data handling in the irene_sankey package.

Functions:
    - _add_suffix_to_cross_column_duplicates: Checks for duplicate values across specified columns
        in each row of a DataFrame, adding suffixes to make each duplicate unique within a row.

Note:
    This module is intended for internal use, and functions here are not part of the public API.
"""

import polars as pl
import logging
from typing import List

logger = logging.getLogger(__name__)


def _add_suffix_to_cross_column_duplicates(
    df: pl.DataFrame, columns: List[str], suffix: str = "-x"
) -> pl.DataFrame:
    """
    Adds suffixes to duplicate values in specified columns within each row of a Polars DataFrame.

    Args:
        df (pl.DataFrame): The input DataFrame.
        columns (List[str]): List of column names to check for cross-column duplicates.
        suffix (str, optional): Suffix to append to duplicate values in each row. Default is "-x".

    Returns:
        pl.DataFrame: Modified DataFrame with suffixes added to duplicates in rows.
    """
    logger.info(f"Starting suffix addition for columns: {columns}")
    df = df.clone()

    # Handle empty DataFrame case
    if df.is_empty():
        return df

    try:

        def process_row(row: tuple) -> tuple:
            seen = {}
            updated_row = list(row)  # Convert tuple to list for modification
            for idx, value in enumerate(row):
                col_name = columns[idx]
                if value not in seen:
                    seen[value] = 1
                else:
                    seen[value] += 1
                    updated_row[idx] = f"{value}{suffix}{seen[value] - 1}"
            return tuple(updated_row)  # Convert back to tuple

        # Apply row-wise transformation using map_rows
        updated_rows = df.select(columns).map_rows(process_row)

        # Convert back into DataFrame with original column names
        updated_df = pl.DataFrame(
            {col: updated_rows[:, i] for i, col in enumerate(columns)}
        )

        # Merge updated columns back into the original DataFrame
        df = df.drop(columns).with_columns(updated_df)

    except Exception as e:
        logger.error(f"Error adding suffix to duplicates: {str(e)}")
        raise

    logger.info("Suffix addition complete")
    return df
