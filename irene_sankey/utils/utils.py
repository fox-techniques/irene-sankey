"""
This module contains internal utility functions for data handling in the irene_sankey package.

Functions:
    - _add_suffix_to_cross_column_duplicates: Checks for duplicate values across specified columns
        in each row of a DataFrame, adding suffixes to make each duplicate unique within a row.

Note:
    This module is intended for internal use, and functions here are not part of the public API.
"""

from ..utils.performance import _log_execution_time

from typing import List
import logging
import pandas as pd

logger = logging.getLogger(__name__)


@_log_execution_time
def _add_suffix_to_cross_column_duplicates(
    df: pd.DataFrame, columns: List[str], suffix: str = "-x"
) -> pd.DataFrame:
    """
    Adds suffixes to duplicate values in specified columns within each row of a DataFrame.

    This function identifies duplicate values across multiple columns within each row of
    the DataFrame and appends a suffix to the second and subsequent occurrences.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (List[str]): List of column names to check for cross-column duplicates.
        suffix (str, optional): Suffix to append to duplicate values in each row. Default is "-x".

    Returns:
        pd.DataFrame: Modified DataFrame with suffixes added to duplicates in rows.
    """
    logger.info(f"Starting suffix addition for columns: {columns}")

    # Make a copy of the DataFrame to avoid side effects
    df = df.copy()

    try:
        for idx, row in df.iterrows():
            seen = {}
            for col in columns:
                value = row[col]
                if value not in seen:
                    seen[value] = 1
                else:
                    seen[value] += 1
                    new_value = f"{value}{suffix}{seen[value] - 1}"
                    df.at[idx, col] = new_value
                    logger.debug(
                        f"Modified duplicate value in row {str(idx)}, column '{col}': {new_value}"
                    )
    except Exception as e:
        logger.error(f"Error adding suffix to duplicates: {str(e)}")
        raise

    logger.info("Suffix addition complete")
    return df
