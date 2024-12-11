import sys

from loguru import logger

logger.add(sys.stderr, format="{time} {level} {message}", filter="my_module", level="INFO")


class Ya360Exception(Exception):

    def __init__(self, message: str):
        self.message = message
        logger.info(message)
        super().__init__(self.message)
