from typing import Optional

import click
from loguru import logger


@click.command()
@click.option(
    "--access-key",
    help="access key to install",
)
@click.option(
    "--version",
    default="latest",
    help="version to install",
)
@click.option(
    "--yes",
    is_flag=True,
    help="install without confirmation",
)
@click.option(
    "--list-versions",
    is_flag=True,
    help="list available versions",
)
def install_toolkit_pro(
    access_key: Optional[str], version: str, yes: bool, list_versions: bool
):
    """DEPRECATED: Use `labelmetk install-pro` instead."""
    logger.error("Deprecated command, please use `labelmetk install-pro` instead.")
    return 1
