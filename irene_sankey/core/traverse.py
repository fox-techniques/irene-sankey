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

import polars as pl
import pandas as pd
from typing import List, Dict, Tuple, Union
import logging

logger = logging.getLogger(__name__)


def traverse_sankey_flow(
    df: Union[pl.DataFrame, pd.DataFrame],
    columns_in_flow: List[str],
    head_node_label: str = "Root",
) -> Tuple[pl.DataFrame, Dict[str, int], Dict[str, List[int]]]:
    """
    Generates a data structure for a Sankey diagram from a DataFrame by chaining columns in the flow.

    Polars is used as the default processing engine. If a Pandas DataFrame is provided, it is converted to Polars first.

    Args:
        df (pl.DataFrame or pd.DataFrame): Input DataFrame with data to chain into a Sankey structure.
        columns_in_flow (List[str]): List of column names to chain sequentially in the Sankey flow.
        head_node_label (str, optional): Label for the root or starting node. Default is "Root".

    Returns:
        Tuple[pl.DataFrame, Dict[str, int], Dict[str, List[int]]]:
            - `flow_df` (pl.DataFrame): DataFrame with columns `source`, `target`, `value`, including indices.
            - `node_map` (Dict[str, int]): Mapping of each unique node to an index.
            - `link` (Dict[str, List[int]]): Dictionary with `source`, `target`, and `value` lists.
    """
    logger.info(f"Starting Sankey flow traversal with columns: {columns_in_flow}")

    if isinstance(df, pd.DataFrame):
        df = pl.from_pandas(df)
    else:
        df = df.clone()

    try:
        # Ensure head node label if needed
        if columns_in_flow[0] in ["", "."]:
            columns_in_flow[0] = "."
            df = df.with_columns(pl.lit(head_node_label).alias("."))
            logger.debug(f"Set head node label to '{head_node_label}'")

        # Collect all unique nodes across specified columns
        unique_nodes = df.select(columns_in_flow).melt().drop("variable").unique()
        all_nodes = unique_nodes["value"].to_list()
        node_map = {node: i for i, node in enumerate(all_nodes)}
        logger.info(f"Created node map with {len(node_map)} unique nodes")

        # Prepare DataFrame for flow links
        flow_df = []

        # Generate links using a sliding window of columns
        for i in range(2, len(columns_in_flow) + 1):
            cols_to_group = columns_in_flow[:i]
            grouped = df.group_by(cols_to_group).agg(pl.len().alias("value"))
            grouped = grouped.select([cols_to_group[-2], cols_to_group[-1], "value"])
            grouped = grouped.rename(
                {cols_to_group[-2]: "source", cols_to_group[-1]: "target"}
            )
            flow_df.append(grouped)

        flow_df = pl.concat(flow_df)

        # Map source and target nodes to indices
        flow_df = flow_df.with_columns(
            pl.col("source").replace(node_map).alias("source_idx"),
            pl.col("target").replace(node_map).alias("target_idx"),
        )

        # Create link dictionary for Sankey diagram
        link = {
            "source": flow_df["source_idx"].to_list(),
            "target": flow_df["target_idx"].to_list(),
            "value": flow_df["value"].to_list(),
        }

    except Exception as e:
        logger.error(f"Error during Sankey flow traversal: {str(e)}")
        raise

    logger.info(f"Sankey flow traversal complete with {str(len(flow_df))} links")
    return flow_df, node_map, link
