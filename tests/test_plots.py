"""
This module contains unit tests for the `plot_irene_sankey_diagram` function 
in the irenesankey package.

Tests:
    - test_plot_irene_sankey_diagram: 
        Tests successful creation of a Sankey diagram figure.
    - test_invalid_color_palette: 
        Tests fallback mechanism for an invalid color palette input.
"""

import pytest
import pandas as pd
from irene_sankey.plots.sankey import plot_irene_sankey_diagram
import plotly.graph_objects as go


@pytest.fixture
def sample_flow_data():
    node_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    flow_df = pd.DataFrame(
        {
            "source": ["A", "B", "C"],
            "target": ["B", "C", "D"],
            "value": [5, 10, 15],
        }
    )
    link = {
        "source": [node_map[src] for src in flow_df["source"]],
        "target": [node_map[tgt] for tgt in flow_df["target"]],
        "value": flow_df["value"].tolist(),
    }
    return node_map, link, flow_df


def test_plot_irene_sankey_diagram(sample_flow_data):
    """Test Sankey diagram plotting with valid data."""
    node_map, link, flow_df = sample_flow_data
    fig = plot_irene_sankey_diagram(node_map, link)
    assert isinstance(fig, go.Figure)


def test_invalid_color_palette(sample_flow_data):
    """Test Sankey diagram with an invalid color palette, should fall back to default."""
    (node_map, link, flow_df) = sample_flow_data
    with pytest.warns(UserWarning, match="Color palette 'InvalidPalette' not found"):
        fig = plot_irene_sankey_diagram(node_map, link, color_palette="InvalidPalette")
    assert isinstance(fig, go.Figure)
