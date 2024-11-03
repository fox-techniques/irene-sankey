# Irene-Sankey  

<img src="https://github.com/fox-techniques/irene-sankey/blob/main/images.logo.png" alt="Irene-Sankey Logo" width="88" align="left" style="margin-right: 10px;"/> Irene-Sankey is a Python library that enables the creation of customizable and informative source-target pair to create Sankey diagrams. It is designed to be intuitive for both beginners and experts, with flexible options for styling, data input, and configuration, making it easy to represent complex flows visually.

[![Python](https://img.shields.io/badge/Python-3.8%2B-darkcyan)](https://pypi.org/project/irene-senkey/)
[![PyPI Latest Release](https://img.shields.io/pypi/v/irene-sankey.svg?label=PyPI%20Version)](https://pypi.org/project/irene-sankey/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/irene-sankey.svg?label=PyPI%20Downloads)](
https://pypi.org/project/irene-sankey/)
[![GitHub](https://img.shields.io/badge/GitHub-irene__sankey-181717?logo=github)](https://github.com/fox-techniques/irene-sankey)
[![License: MIT](https://img.shields.io/badge/License-MIT-orange.svg)](https://github.com/fox-techniques/irene-sankey/blob/main/LICENSE)

## Table of Contents

- [Irene-Sankey](#irene-sankey)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Installation](#installation)
  - [Quick Start](#quick-start)
  - [Usage](#usage)
  - [Documentation](#documentation)
  - [Contribution](#contribution)
  - [License](#license)
  - [Acknowledgments](#acknowledgments)


## Overview

**Irene-Sankey** offers an easy-to-use interface for creating Sankey diagrams, which are ideal for visualizing flow distributions across different categories or entities. The package is built to work seamlessly with pandas data structures and provides a range of customization options for colors, labels, and node arrangements, making it perfect for data analysts, data scientists, and anyone interested in visualizing complex flows.


## Features

- **Simple Sankey Diagrams**: Easily create source-target pair and customize Sankey diagrams from pandas DataFrames.
- **Customizable Styles**: Customize colors, labels, node spacing, and flow thickness to suit your needs.
- **Support for Large Diagrams**: Efficiently handles larger flows and multiple nodes.
- **Integrates with Pandas**: Easily map columns and rows from pandas DataFrames to nodes and links.


## Installation

Install **Irene-Sankey** using pip:

```bash
pip install irene_sankey
```

> **Note**: Requires Python 3.8 or above.


## Quick Start

Here’s a quick example to create a simple Sankey diagram with **Irene-Sankey**.

```python
import pandas as pd
from irene_sankey.core.traverse import traverse_sankey_flow
from irene_sankey.plots.sankey import plot_irene_sankey_diagram

# Sample data to test the functionality
df = pd.DataFrame(
    {
        "country": ["NL","NL","NL","DE","DE","FR","FR","FR","US","US","US"],
        "industry": [
            "Technology","Finance","Healthcare",
            "Automotive","Engineering",
            "Technology","Agriculture","Healthcare",
            "Manufacturing","Technology","Finance"],
        "field": [
            "Software","Banking","Pharmaceuticals",
            "Car Manufacturing","Mechanical Engineering",
            "Software","Crop Science","Medical Devices",
            "Electronics","AI & Robotics","Investment Banking"],
    }
)

# Generate source-target pair, node map and link for Sankey diagrams
flow_df, node_map, link = traverse_sankey_flow(df, ["", "country", "industry", "field"])

# Plot Sankey diagram 
fig = plot_irene_sankey_diagram(node_map, link, title = "Irene-Sankey Demo", node_config={
        "pad": 10,
        "line": dict(color="black", width=1),
    }
)
fig.show()
```

## Usage

The core class in the **Irene-Sankey** package is `traverse_sankey_flow`. By passing a pandas DataFrame and selecting string columns in the order of the flow, you can quickly generate a required source-targer pair map to generate Sankey diagram.


## Documentation

Detailed documentation for **Irene-Sankey**, including all available methods and customization options, will be available at:

[Irene-Sankey Documentation](https://github.com/fox-techniques/irene-sankey/wiki)



## Contribution

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a branch (`git checkout -b feature/NewFeature`).
3. Commit your changes (`git commit -m 'Add NewFeature'`).
4. Push to the branch (`git push origin feature/NewFeature`).
5. Open a Pull Request.


## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/fox-techniques/irene-sankey/blob/main/LICENSE) file for details.


## Acknowledgments

I would like to express my heartfelt gratitude to everyone who contributed their knowledge and support, making this project possible. Special thanks to [Mike Bostock](https://observablehq.com/@mbostock) and [Yan Holtz](https://www.yan-holtz.com/) for their invaluable inspiration and insights, which profoundly influenced the direction and development of this project. Their expertise and knowledge were instrumental in shaping its final form. I am also grateful to the Plotly team for their incredible library, enabling the creation of beautiful, interactive visualizations that bring the data to life.

Special thanks to the contributors and the open-source community for their support and feedback. The Sankey visualization method is inspired by [Matplotlib's Sankey capabilities](https://matplotlib.org/stable/gallery/specialty_plots/sankey_basics.html), with enhancements for customization and usability.
