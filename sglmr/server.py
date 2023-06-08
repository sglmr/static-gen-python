import logging
from os import system
from pathlib import Path

logger = logging.getLogger(__name__)


def serve(directory: Path, port=8000):
    try:
        cmd = f"python -m http.server {port} --directory {directory}"
        system(cmd)
    except KeyboardInterrupt:
        logger.warning("Server keyboard interrupt")
