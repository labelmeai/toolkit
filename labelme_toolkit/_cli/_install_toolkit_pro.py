import os.path as osp
import subprocess
import urllib.request

import click
from loguru import logger


@click.command()
@click.option(
    "--access-key",
    prompt=True,
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
def install_toolkit_pro(access_key: str, version: str, yes: bool, list_versions: bool):
    """Install Toolkit Pro.

    Examples:

     \b
     $ labelmetk install-toolkit-pro  # install latest
     $ labelmetk install-toolkit-pro --version 1.0.0
     $ labelmetk install-toolkit-pro --access-key xxxxxxxx

    """
    logger.info("Installing the Labelme Toolkit Pro...")
    logger.info(f"Access key: {access_key}")

    url_path = f"https://labelmeai.github.io/toolkit-pro/{access_key}"

    with urllib.request.urlopen(osp.join(url_path, "versions")) as response:
        data = response.read()
        versions = [version.strip() for version in data.decode("utf-8").splitlines()]

    if list_versions:
        for version in versions:
            click.echo(version)
        return

    if version == "latest":
        version = versions[-1]
        logger.info(f"Installing version: {version} (latest)")
    elif version not in versions:
        logger.error(f"Version {version} is not available")
        return
    else:
        logger.info(f"Installing version: {version}")

    if not yes:
        if not click.confirm("Do you want to install?"):
            click.echo("Installation is canceled.")
            return

    cmd = [
        "pip",
        "install",
        "-I",
        osp.join(url_path, f"labelme_toolkit_pro-{version}-py3-none-any.whl"),
    ]
    logger.info(f"Running command: {' '.join(cmd)}")
    try:
        subprocess.check_call(cmd)
    except subprocess.CalledProcessError:
        logger.error("Failed to install. Is the access key correct?")
        return
