import logging
import os

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
    
    log_dir = "backend/logs"
    os.makedirs(log_dir, exist_ok=True)

    if not logger.handlers:
        fh = logging.FileHandler(os.path.join(log_dir, "sqlite_clone.log"), mode='a', encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger
