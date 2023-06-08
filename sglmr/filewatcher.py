import logging
from time import sleep

from builder import build
from config import Config

logger = logging.getLogger(__name__)


def filewatcher(config: Config = Config()):
    try:
        last_mtime = 0
        latest_mtime = 0
        while True:
            for path in config.CONTENT_DIR.glob("**/*"):
                latest_mtime = max(latest_mtime, path.stat().st_mtime)

            if latest_mtime > last_mtime:
                build(config=config)
                last_mtime = latest_mtime

            sleep(1)
    except KeyboardInterrupt:
        logger.info("Filewatcher keyboard interrupt")
