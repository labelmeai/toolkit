import sys

import click
from loguru import logger

from labelme_toolkit import __version__


@click.group(context_settings=dict(help_option_names=["-h", "--help"]))
@click.version_option(__version__)
def cli():
    logger.remove()
    logger.add(
        sys.stderr, level="INFO", colorize=True, format="<level>{message}</level>"
    )


from labelme_toolkit._cli import _extract_image  # noqa
from labelme_toolkit._cli import _json_to_mask  # noqa
from labelme_toolkit._cli import _json_to_visualization  # noqa
from labelme_toolkit._cli import _list_labels  # noqa
from labelme_toolkit._cli import _install_toolkit_pro  # noqa
