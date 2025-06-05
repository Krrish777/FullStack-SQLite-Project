import logging

def get_logger(name):
    """
    Creates and returns a logger instance with a file handler.

    The logger writes logs to 'sqlite_clone.log' and includes timestamps, logger names,
    log levels, and messages in the log entries. It ensures that multiple handlers are not added.

    Args:
        name (str): The name of the logger (usually __name__).

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.encoding = 'utf-8'

    if not logger.handlers:
        fh = logging.FileHandler("sqlite_clone.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
