import sys

import click
from loguru import logger

from .. import __version__
from ._ai_annotate_rectangles import ai_annotate_rectangles
from ._extract_image import extract_image
from ._install_pro import install_pro
from ._install_toolkit_pro import install_toolkit_pro
from ._json_to_mask import json_to_mask
from ._json_to_visualization import json_to_visualization
from ._list_labels import list_labels


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
def cli():
    logger.remove()
    logger.add(
        sys.stderr, level="INFO", colorize=True, format="<level>{message}</level>"
    )


cli.add_command(ai_annotate_rectangles)
cli.add_command(extract_image)
cli.add_command(install_pro)
cli.add_command(install_toolkit_pro)
cli.add_command(json_to_mask)
cli.add_command(json_to_visualization)
cli.add_command(list_labels)

try:
    from labelme_toolkit_pro import COMMANDS

    for command in COMMANDS:
        cli.add_command(command)
except ImportError:
    pass
