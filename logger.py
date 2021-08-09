import logging
from logging.handlers import RotatingFileHandler


logger = logging.getLogger()
logger.addHandler(RotatingFileHandler('out.log', maxBytes=1024 * 1024, backupCount=1))
logger.setLevel(logging.INFO)
