"""
This module contains unit tests for the `traverse_sankey_chain` function in the irenesankey package.

Tests:
    - test_traverse_sankey_chain: 
        Tests standard chaining of columns to create Sankey data structure.
    - test_traverse_with_head_node: 
        Tests functionality with a custom head node label.
    - test_traverse_empty_df: 
        Verifies handling of an empty DataFrame.
    - test_traverse_invalid_input: 
        Tests error handling for missing or invalid columns.
"""

import pytest
import pandas as pd
from irene_sankey.core.traverse import traverse_sankey_flow


@pytest.fixture
def sample_df():
    return pd.DataFrame(
        {
            "Stage1": ["A", "B", "A", "C"],
            "Stage2": ["B", "C", "B", "D"],
            "Stage3": ["C", "D", "D", "E"],
        }
    )


def test_traverse_sankey_chain(sample_df):
    """Test standard chaining of columns."""
    flow_df, node_map, link = traverse_sankey_flow(
        sample_df, ["Stage1", "Stage2", "Stage3"]
    )

    assert "source" in flow_df.columns
    assert "target" in flow_df.columns
    assert "value" in flow_df.columns
    assert isinstance(node_map, dict)
    assert isinstance(link, dict)
    assert set(link.keys()) == {"source", "target", "value"}


def test_traverse_with_head_node(sample_df, head_node_label="TestRoot"):
    """Test that head node label is correctly applied."""
    flow_df, node_map, link = traverse_sankey_flow(
        sample_df, ["", "Stage1", "Stage2", "Stage3"], head_node_label
    )

    assert head_node_label in node_map  # Head node column replacement
    assert node_map[head_node_label] == node_map[head_node_label]


def test_traverse_empty_df():
    """Test with an empty DataFrame."""
    df = pd.DataFrame(columns=["Stage1", "Stage2", "Stage3"])
    flow_df, node_map, link = traverse_sankey_flow(df, ["Stage1", "Stage2", "Stage3"])
    assert flow_df.empty
    assert node_map == {}
    assert link == {"source": [], "target": [], "value": []}


def test_traverse_invalid_input():
    """Test with invalid input, such as missing columns."""
    df = pd.DataFrame({"col1": ["A", "B"], "col2": ["C", "D"]})
    with pytest.raises(KeyError):
        traverse_sankey_flow(df, ["Stage1", "Stage2"])
