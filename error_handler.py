# workflow/error_handler.py
import time
import logging
from typing import Callable, Any, Dict

logger = logging.getLogger("ErrorHandler")

def with_retry(max_retries: int = 3, backoff_factor: float = 1.5):
    """Decorator that retries a node function upon exception with backoff delay."""
    def decorator(func: Callable):
        def wrapper(state: Dict[str, Any], *args, **kwargs) -> Dict[str, Any]:
            retries = 0
            while retries < max_retries:
                try:
                    return func(state, *args, **kwargs)
                except Exception as e:
                    retries += 1
                    sleep_time = backoff_factor ** retries
                    logger.warning(
                        f"[BUG-013 Retry] Node '{func.__name__}' failed (Attempt {retries}/{max_retries}). "
                        f"Error: {e}. Retrying in {sleep_time:.1f}s..."
                    )
                    time.sleep(sleep_time)
            
            logger.error(f"[BUG-013 Fallback] Node '{func.__name__}' failed after {max_retries} attempts. Triggering fallback.")
            return {}
        return wrapper
    return decorator