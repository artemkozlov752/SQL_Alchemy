import logging.config
import os
import re
import yaml


def get_config(path_to_yaml_config: str):
    """Read configs from yaml.

    Args:
        path_to_yaml_config (str): path to config

    Returns:
        (dict).

    """
    with open(path_to_yaml_config, encoding='utf-8') as fin:
        config = yaml.safe_load(fin)
    return config


def logger_initializing(path_to_logger: str):
    """Initialize logger wrt to config.

    Args:
        path_to_logger (str): path to logger yaml config.

    """
    with open(path_to_logger, 'r') as stream:
        config = yaml.safe_load(stream)
    path_to_logs = config["handlers"]["info_file_handler"]["filename"]
    create_directory_if_not_exists(path_to_logs)
    logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.info('logger has been initialized')


def create_directory_if_not_exists(path_to_file: str):
    """Check existence of the directory and create it if it does not exist.

    Args:
        path_to_file (str): path to file

    """
    directory = re.findall("(\.\/.*)\/(.*)", path_to_file)[0][0]
    if not os.path.exists(directory):
        os.makedirs(directory)
