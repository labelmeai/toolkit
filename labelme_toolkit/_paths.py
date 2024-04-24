import glob
import os
from typing import List
from typing import Tuple

from loguru import logger

from . import _formats


def get_json_files_and_output_dir(file_or_dir: str) -> Tuple[List[str], str]:
    if not os.path.exists(file_or_dir):
        raise FileNotFoundError(f"File or directory not found: {file_or_dir!r}")

    file_or_dir = os.path.normpath(file_or_dir)

    json_files: List[str]
    if os.path.isfile(file_or_dir):
        json_files = [file_or_dir]
    else:
        json_files = sorted(glob.glob(os.path.join(file_or_dir, "*.json")))
    logger.info(
        f"Found {len(json_files)} JSON files: {_formats.pformat_list(json_files)}"
    )

    if os.path.isfile(file_or_dir):
        output_dir_prefix = os.path.splitext(file_or_dir)[0]
    else:
        output_dir_prefix = file_or_dir

    output_dir: str = f"{output_dir_prefix}.export"

    return json_files, output_dir
