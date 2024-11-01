"""
This module provides the `plot_irene_sankey_diagram` function, which generates a Sankey
diagram using Plotly based on flow data and node mappings provided.

Functions:
    - plot_irene_sankey_diagram: Creates a Sankey diagram figure from provided flow data, 
        node mapping, and links, with customizable color palettes.

Example usage:
    from irene_sankey.plots.sankey import plot_irene_sankey_diagram

    fig = plot_irene_sankey_diagram(node_map, link)
    fig.show()
"""

import plotly.express as px
import plotly.graph_objects as go

from ..utils.performance import _log_execution_time

from typing import List, Dict

import logging
import warnings

logger = logging.getLogger(__name__)


@_log_execution_time
def plot_irene_sankey_diagram(
    node_map: Dict[str, int],
    link: Dict[str, List[int]],
    color_palette: str = "Dark24_r",
) -> go.Figure:
    """
    Plots a Sankey diagram using flow data, node mapping, and link information.

    This function generates a Sankey diagram using `plotly`, with nodes and links
    specified by the input flow DataFrame and link dictionary. The color palette
    can be customized to a predefined Plotly palette.

    Args:
        node_map (Dict[str, int]): Mapping of node labels to node indices for use in the diagram.
        link (Dict[str, List[int]]): Dictionary with lists of `source`, `target`, and `value`
            indices for Sankey links.
        color_palette (str, optional): Plotly color palette name, default is "Dark24_r".

    Returns:
        go.Figure: Plotly Figure object of the generated Sankey diagram.
    """
    logger.info(f"Plotting Irene-Sankey diagram with '{color_palette}' color palette.")

    try:
        node_labels = list(node_map.keys())
        num_nodes = len(node_labels)
        logger.info(f"Creating Sankey diagram with {str(num_nodes)} nodes")

        # Validate color palette
        try:
            qualitative_colors = getattr(px.colors.qualitative, color_palette)
            logger.debug(f"Using color palette: {color_palette}")
        except AttributeError:
            logger.warning(f"Color palette '{color_palette}' not found, using default")
            warnings.warn(
                f"Color palette '{color_palette}' not found, using default 'Dark24_r'",
                UserWarning,
            )

            qualitative_colors = px.colors.qualitative.Dark24_r

        # Assign colors to each node
        node_colors = [
            qualitative_colors[i % len(qualitative_colors)] for i in range(num_nodes)
        ]

        # Create the Sankey diagram
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        pad=10,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=node_labels,
                        color=node_colors,
                    ),
                    link=link,
                    arrangement="freeform",
                )
            ]
        )

        fig.update_layout(title_text="Sankey Chain Diagram", font_size=12)

    except Exception as e:
        logger.error(f"Failed to create Sankey diagram: {str(e)}")
        raise

    logger.info("Sankey diagram created successfully")
    return fig
