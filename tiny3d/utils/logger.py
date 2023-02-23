import logging

initialized_logger = {}

def get_logger(logger_name='tiny3d', log_level=logging.INFO, log_file=None):
    logger = logging.getLogger(logger_name)
    if logger_name in initialized_logger:
        return logger

    format_str = '[%(asctime)s %(filename)s] %(levelname)s: %(message)s'
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter(format_str))
    logger.addHandler(stream_handler)
    logger.propagate = False
    logger.setLevel(log_level)
    if log_file is not None:
        logger.setLevel(log_level)
        # add file handler
        file_handler = logging.FileHandler(log_file, 'w')
        file_handler.setFormatter(logging.Formatter(format_str))
        file_handler.setLevel(log_level)
        logger.addHandler(file_handler)
    initialized_logger[logger_name] = True
    return logger
