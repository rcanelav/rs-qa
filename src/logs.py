import logging
import logging.config


def configure_logging(log_level="INFO", log_to_file=False, log_file_path="app.log"):
    """
    Configures logging for the application.

    Args:
        log_level (str): Logging level (e.g., "DEBUG", "INFO", "WARNING"). Default is "INFO".
        log_to_file (bool): Whether to log to a file. Default is False.
        log_file_path (str): Path to the log file. Default is "app.log".
    """
    # Set up logging handlers
    handlers = {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'detailed',
            'stream': 'ext://sys.stdout',
        }
    }

    # Configure file handler
    if log_to_file:
        handlers['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'detailed',
            'filename': log_file_path,
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
        }

    # Configure the logging structure
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - [%(filename)s:%(lineno)d]',
            },
        },
        'handlers': handlers,
        'root': {
            'level': log_level.upper(),
            'handlers': list(handlers.keys()),
        },
    }

    # Apply the logging configuration
    logging.config.dictConfig(logging_config)

    # CHECK
    logger = logging.getLogger("CONFIG")
    logger.info("Logging is configured.")
