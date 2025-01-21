import os
import sys

import click
from loguru import logger

from .. import __version__
from ._ai_annotate_rectangles import ai_annotate_rectangles
from ._extract_image import extract_image
from ._install_pro import install_pro
from ._json_to_mask import json_to_mask
from ._json_to_visualization import json_to_visualization
from ._list_labels import list_labels


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
def cli():
    logger.remove(0)

    def format_console(record: dict):
        # 1. don't show any tracebacks in the console
        # 2. show the level of the log message when it's >= WARNING
        if record["level"].no >= 30:  # 30 = WARNING
            return (
                f"<level>{record['level'].name.lower()}:</level> {record['message']}\n"
            )
        else:
            return f"{record['message']}\n"

    logger.add(
        sys.stderr,
        level="INFO",
        colorize=True,
        format=format_console,
        backtrace=False,
        diagnose=False,
    )
    os.makedirs(os.path.expanduser("~/.cache/labelme"), exist_ok=True)
    logger.add(
        os.path.expanduser("~/.cache/labelme/toolkit.log"), colorize=True, level="DEBUG"
    )


cli.add_command(ai_annotate_rectangles)
cli.add_command(extract_image)
cli.add_command(install_pro)
cli.add_command(json_to_mask)
cli.add_command(json_to_visualization)
cli.add_command(list_labels)

try:
    from labelme_toolkit_pro import COMMANDS

    for command in COMMANDS:
        cli.add_command(command)
except ImportError:
    pass
