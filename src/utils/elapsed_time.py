import datetime
import logging

logger = logging.getLogger("ELAPSED_TIME")


def elapsed_time(metric_name_func):
    """Calculate the elapsed time of a function and log it.
       The metric_name_func is a callable that returns the metric name."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = datetime.datetime.now()
            metric_name = metric_name_func()
            result = func(*args, **kwargs)
            end_time = datetime.datetime.now()
            logger.info(
                f"### {metric_name} ELAPSED TIME: {end_time - start_time}")
            return result
        return wrapper
    return decorator
