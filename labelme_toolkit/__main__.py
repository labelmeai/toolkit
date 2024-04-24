import sys

from loguru import logger

from labelme_toolkit._cli import cli


def main():
    try:
        cli()
    except Exception as e:
        logger.exception(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
