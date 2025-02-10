import logging
import datetime
import os
import sys

from bms.api import make_server

logger = logging.getLogger("bms")
now = datetime.datetime.now()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s|%(levelname)s:%(name)s:%(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S",
    encoding="utf-8",
    handlers=[
        logging.FileHandler(os.path.join('/bms', 'logs', f"logs_{now.strftime('%Y-%m-%dT%H:%M:%S')}.log")),
        logging.StreamHandler(sys.stdout)
    ]
)

app = make_server()
