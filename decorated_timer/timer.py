"""Module to log the execution time of functions."""
import logging
import time
from functools import wraps
from typing import Any, Callable, Optional


# Function to safely truncate arguments for logging
def truncate(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


# Function to remove sensitive parameters from kwargs
def filter_sensitive_params(kwargs: dict) -> dict:
    """Filter out sensitive parameters from kwargs."""
    return {k: v for k, v in kwargs.items() if not (k.startswith("_") or k.startswith("__"))}


def timer_logger(func: Any) -> Callable:
    """Decorate a function to log the execution time."""

    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        """Wrap the function to log the execution time."""
        # Filter out sensitive kwargs
        safe_kwargs = filter_sensitive_params(kwargs)
        # Truncate args and safe_kwargs for safe logging
        truncated_args = truncate(str(args))
        truncated_kwargs = truncate(str(safe_kwargs))
        # Log the function name and input arguments
        logging.info(
            f"Function '{func.__name__}' called at {time.strftime('%Y-%m-%d %H:%M:%S')} with args: {truncated_args} and kwargs: {truncated_kwargs}"
        )

        start_time = time.time()  # Record the start time
        try:
            # Execute the function
            result = func(*args, **kwargs)  # noqa
            return result  # noqa
        except Exception:
            # Log any exceptions that occur
            logging.exception(f"An error occurred in function '{func.__name__}'")  # noqa
            raise  # Re-raise the exception after logging
        finally:
            # Record the end time and log the duration
            end_time = time.time()
            duration = end_time - start_time
            logging.info(
                f"Function '{func.__name__}' finished at {time.strftime('%Y-%m-%d %H:%M:%S')} with duration {duration:.4f} seconds"
            )

    return wrapper

if __name__ == "__main__":
    # Example usage of the timer_logger decorator
    # This function will be logged when called
    @timer_logger
    def example_function(
        arg1: str,
        arg2: str,
        _sensitive_param: Optional[str] = None,
        __confidential_data: Optional[str] = None,
        kwarg1: Optional[str] = None,
    ) -> str:
        """Demonstrate the timer_logger decorator."""
        time.sleep(1)
        return "Result"


    example_function(
        "arg1",
        "arg2",
        _sensitive_param="should not be logged",
        __confidential_data="should also not be logged",
        kwarg1="kwarg1",
    )
