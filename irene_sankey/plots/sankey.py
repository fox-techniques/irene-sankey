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
    title: str = "Irene-Sankey Flow Diagram",
    **kwargs,
) -> go.Figure:
    """
    Plots a Sankey diagram using flow data, node mapping, and link information.

    This function generates a Sankey diagram using `plotly`, with nodes and links
    specified by the input flow DataFrame and link dictionary. The color palette
    can be customized to a predefined Plotly palette, and additional layout
    options can be passed via `kwargs`.

    Args:
        node_map (Dict[str, int]): Mapping of node labels to node indices for use in the diagram.
        link (Dict[str, List[int]]): Dictionary with lists of `source`, `target`, and `value`
            indices for Sankey links.
        color_palette (str, optional): Plotly color palette name, default is "Dark24_r".
        title (str, optional): Plot's title, default is "Irene-Sankey Flow Diagram".
        **kwargs: Additional keyword arguments to customize the layout or node settings.

    Returns:
        go.Figure: Plotly Figure object of the generated Sankey diagram.
    """
    logger.info(f"Plotting Irene-Sankey diagram with '{color_palette}' color palette.")

    try:
        node_labels = list(node_map.keys())
        num_nodes = len(node_labels)
        logger.info(f"Creating Irene-Sankey diagram with {num_nodes} nodes")

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

        # Extract any node-specific options passed in kwargs, defaulting if not provided
        node_config = kwargs.pop("node_config", {})
        node_config.setdefault("pad", 10)
        node_config.setdefault("thickness", 20)
        node_config.setdefault("line", dict(color="black", width=0.5))

        # Create the Sankey diagram
        fig = go.Figure(
            data=[
                go.Sankey(
                    node=dict(
                        label=node_labels,
                        color=node_colors,
                        **node_config,  # Apply node configuration
                    ),
                    link=link,
                    arrangement="freeform",
                )
            ]
        )

        # Apply layout settings using additional kwargs
        fig.update_layout(title_text=title, **kwargs)

    except Exception as e:
        logger.error(f"Failed to create Irene-Sankey diagram: {str(e)}")
        raise

    logger.info("Irene-Sankey diagram is created successfully")
    return fig
