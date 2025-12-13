import logging
import sys
import os

LOG_FOLDER = "../logs"
LOG_FILE_NAME = "app.log"

def get_logger(name: str = None) -> logging.Logger:
    """Returns a named logger that inherits from the root logger."""
    return logging.getLogger(name)

def get_log_file():
    os.makedirs(LOG_FOLDER, exist_ok=True)
    return os.path.join(LOG_FOLDER, LOG_FILE_NAME)

def log_marker(logger, marker: str, symbol: str = "=", size: int = 20):
    """Logs a visual marker with customizable symbol and size."""
    output = f"{symbol * size} {marker} {symbol * size}"
    logger.info(output)

def setup_root_logger(log_level=logging.INFO):
    """Sets up the root logger with console and file handlers. This should be called only once at startup."""
    # remove existing handlers so we can set up our own
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    root_logger = logging.getLogger()
    if not root_logger.handlers:
        root_logger.setLevel(log_level)

        # Create formatter
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        # File handler
        file_handler = logging.FileHandler(get_log_file())
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)

        # Add handlers
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

        # Optional: prevent logs from being propagated to ancestor loggers
        root_logger.propagate = False


