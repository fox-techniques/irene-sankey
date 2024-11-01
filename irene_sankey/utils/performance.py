"""
This module provides a decorator for logging the execution time of functions
within the irenesankey package. It is useful for performance monitoring and 
optimizing code by identifying functions that may be computationally intensive.

Classes and Decorators:
    - _log_execution_time: A decorator that measures and logs the time a function
        takes to execute. This helps in performance profiling and maintaining 
        awareness of processing time, especially for functions handling large datasets.

Example usage:
    from irene_sankey.utils.performance import log_execution_time

    @_log_execution_time
    def example_function():
        # Function code here

    example_function()  # Execution time will be logged
"""

import time
import logging

from functools import wraps
from typing import Callable, Any

logger = logging.getLogger(__name__)


def _log_execution_time(func: Callable) -> Callable:
    """
    A decorator that logs the execution time of the decorated function.

    This decorator is applied to functions to measure the time taken to execute them.
    Upon completion, it logs the time in seconds with the function name for easy
    identification in the logs. It is particularly useful for profiling functions that
    handle large datasets or perform complex calculations.

    Args:
        func (Callable): The function whose execution time should be measured.

    Returns:
        Callable: The wrapped function with added timing functionality.

    Example:
        @_log_execution_time
        def some_function():
            pass
    """

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        elapsed_time = end_time - start_time
        logging.getLogger(__name__).info(
            "Executed %s in %.4f seconds", func.__name__, elapsed_time
        )
        return result

    return wrapper
