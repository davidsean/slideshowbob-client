import os
import logging

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

if os.environ.get('PAGE_ACCESS_TOKEN', None) is None or os.environ.get('SUB_PASSWORD',None) is None or os.environ.get('TOPIC', None) is None:
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.critical("Missing contents from .env file")
    raise ValueError
