"""
This module provides the `traverse_sankey_flow` function for creating a Sankey diagram
data structure from a DataFrame by sequentially chaining specified columns.

Functions:
    - traverse_sankey_flow: Constructs a Sankey diagram data structure by chaining 
        specified columns in the provided DataFrame. Handles duplicate values by using 
        an internal utility function to add suffixes to duplicate values within rows.

Example usage:
    from irene_sankey.core.traverse import traverse_sankey_flow

    flow_df, node_map, link = traverse_sankey_flow(
        df, ["Stage1", "Stage2", "Stage3"], head_node_label="Root"
    )
"""

import pandas as pd

from ..utils.utils import _add_suffix_to_cross_column_duplicates
from ..utils.performance import _log_execution_time

from typing import List, Dict, Tuple

import logging

logger = logging.getLogger(__name__)


@_log_execution_time
def traverse_sankey_flow(
    df: pd.DataFrame,
    columns_in_flow: List[str],
    head_node_label: str = "Root",
) -> Tuple[pd.DataFrame, Dict[str, int], Dict[str, List[int]]]:
    """
    Generates a data structure for a Sankey diagram from a DataFrame by chaining columns in the flow.

    This function creates a flow data structure based on sequential flow of columns
    from a DataFrame. Each flow step in specified columns is linked in sequence,
    allowing the creation of a Sankey diagram to visualize the flow.

    Args:
        df (pd.DataFrame): Input DataFrame with data to chain into a Sankey structure.
        columns_in_flow (List[str]): List of column names to chain sequentially in the Sankey flow.
            An empty string or period in the first position represents the head node.
        head_node_label (str, optional): Label for the root or starting node,
            default is "Root".

    Returns:
        Tuple[pd.DataFrame, Dict[str, int], Dict[str, List[int]]]:
            - `flow_df` (pd.DataFrame): DataFrame with columns `source`, `target`,
                and `value`, including indices for node mapping.
            - `node_map` (Dict[str, int]): Mapping of each unique node to an index.
            - `link` (Dict[str, List[int]]): Dictionary containing lists of `source`,
                `target`, and `value` indices for each link in the Sankey diagram.
    """
    logger.info(f"Starting Sankey flow traversal with columns: {columns_in_flow}")

    # Make a copy of the DataFrame to avoid side effects
    df = df.copy()

    try:
        # Ensure head node label if needed
        if columns_in_flow[0] == "" or columns_in_flow[0] == ".":
            columns_in_flow[0] = "."
            df["."] = head_node_label
            logger.debug(f"Set head node label to '{head_node_label}'")

        # Handle columns duplicates
        df = _add_suffix_to_cross_column_duplicates(df, columns=columns_in_flow)
        logger.info(f"Handled duplicates in columns: {columns_in_flow}")

        # Collect all unique nodes across specified columns
        all_nodes = pd.unique(df[columns_in_flow].stack())
        node_map = {node: i for i, node in enumerate(all_nodes)}
        logger.info(f"Created node map with {len(node_map)} unique nodes")

        # Prepare DataFrame for flow links
        flow_df = pd.DataFrame(columns=["source", "target", "value"])

        # Generate links using a sliding window of columns
        for i in range(2, len(columns_in_flow) + 1):
            # Select the expanding window of columns
            cols_to_group = columns_in_flow[:i]

            # Group by the selected columns and sum the values
            grouped = df.groupby(cols_to_group).size().reset_index(name="value")

            # Extract the last two columns and append them along with the 'value' column
            grouped = grouped[[cols_to_group[-2], cols_to_group[-1], "value"]]

            # Rename the columns for consistency
            grouped.columns = ["source", "target", "value"]

            # Append the result to the final DataFrame
            flow_df = pd.concat([flow_df, grouped])

        # Map source and target nodes to indices
        flow_df["source_idx"] = flow_df["source"].map(node_map)
        flow_df["target_idx"] = flow_df["target"].map(node_map)

        # Create link dictionary for Sankey diagram
        link = {
            "source": flow_df["source_idx"].tolist(),
            "target": flow_df["target_idx"].tolist(),
            "value": flow_df["value"].tolist(),
        }

    except Exception as e:
        logger.error(f"Error during Sankey flow traversal: {str(e)}")
        raise

    logger.info(f"Sankey flow traversal complete with {str(len(flow_df))} links")
    return flow_df, node_map, link
