import logging


def setup_logger(name, log_file='server.log', level=logging.DEBUG):
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(name)

    # Config the custom logger
    logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)

    return logger
