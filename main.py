"""
Test task for working with sql table.
For more information see the link:
https://gist.github.com/anonymous/c4b9108779932792270e

copyright: (c) 2019 by Artem Kozlov.

"""


import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.engine.url import URL

from OrderCode.order import fill_test_data, Base, get_data_by_chunks
from util import get_config, logger_initializing


PATH_TO_CONFIG = "./configs/config.yaml"
CONFIG = get_config(PATH_TO_CONFIG)


def main():
    logger_initializing(CONFIG["path_to_logger"])
    logger = logging.getLogger(__name__)

    logger.info("Engine initializing")
    engine = create_engine(URL(**CONFIG["credentials"]), echo=False)
    logger.debug(f"Host {CONFIG['credentials']['host']}, port {CONFIG['credentials']['port']} in use")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    logger.info("Session initializing")
    session = Session(engine)

    logger.info("Filling sql-base with testing data is in process")
    fill_test_data(CONFIG["test_data_length"], session)
    logger.info("Get data by chunks")
    get_data_by_chunks(CONFIG["batch_size"], session)


if __name__ == "__main__":
    main()
