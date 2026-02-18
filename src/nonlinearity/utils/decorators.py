"""
Decorator utilities.

Common decorators for timing and logging.
"""

import functools
import time
from typing import Callable


def timer(func: Callable) -> Callable:
    """
    Decorator to measure function execution time.
    
    Args:
        func: Function to time.
    
    Returns:
        Wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"{func.__name__} took {elapsed:.2f} seconds")
        return result
    return wrapper


def log_calls(func: Callable) -> Callable:
    """
    Decorator to log function calls.
    
    Args:
        func: Function to log.
    
    Returns:
        Wrapped function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} completed")
        return result
    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """
    Decorator to retry a function on failure.
    
    Args:
        max_attempts: Maximum number of attempts.
        delay: Delay between attempts in seconds.
    
    Returns:
        Decorator function.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise
                    print(f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {e}")
                    time.sleep(delay)
        return wrapper
    return decorator
