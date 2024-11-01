from .core.traverse import traverse_sankey_flow
from .plots.sankey import plot_irene_sankey_diagram

from .utils.performance import _log_execution_time

import logging


# Set up default logging configuration
@_log_execution_time
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=level
    )


# Initialize logging with INFO level by default
setup_logging()

# Package-level imports
__all__ = ["traverse_sankey_flow", "plot_irene_sankey_diagram"]

__version__ = "0.1.0"
