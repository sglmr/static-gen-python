import argparse
import logging
from concurrent.futures import ProcessPoolExecutor
from sys import argv
from time import sleep

from builder import build
from config import Config
from filewatcher import filewatcher
from server import serve

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    from rich.logging import RichHandler

    # Basic logging config
    logging.basicConfig(
        format="%(name)s: %(message)s",
        datefmt="[%X]",
        level=logging.INFO,
        handlers=[RichHandler()],
    )

    parser = argparse.ArgumentParser(
        description="Build a static site.",
        epilog="Cheers!",
    )

    parser.add_argument(
        "-l",
        "--listen",
        dest="listen",
        action="store_true",
        help="Serve files via HTTP and port 8000",
    )

    parser.add_argument(
        "-r",
        "--autoreload",
        dest="autoreload",
        action="store_true",
        help="Rebuild site each time a modification occurs" " on the content files.",
    )

    args = parser.parse_args(argv[1:])
    config = Config()

    try:
        if args.autoreload and args.listen:
            with ProcessPoolExecutor(max_workers=2) as executor:
                executor.submit(serve, config.OUTPUT_DIR)
                executor.submit(sleep(0.1))
                executor.submit(filewatcher, config)
        elif args.listen:
            # Run build command
            build(config=config)
            serve(directory=config.OUTPUT_DIR)
        else:
            build(config=config)

    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt on main")
