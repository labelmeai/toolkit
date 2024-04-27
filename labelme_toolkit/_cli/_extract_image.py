import json
import os
from typing import Dict
from typing import List

import click
import PIL.Image
from loguru import logger

from .. import _json
from .. import _migrations
from .. import _paths


def _extract_image(json_file: str, output_dir: str) -> None:
    with open(json_file) as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    image: PIL.Image.Image
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = PIL.Image.open(image_path)
    else:
        image = PIL.Image.fromarray(
            _json.image_b64data_to_ndarray(json_data["imageData"])
        )

    os.makedirs(output_dir, exist_ok=True)

    output_image_file = os.path.join(
        output_dir, os.path.splitext(os.path.basename(json_file))[0] + ".jpg"
    )
    image.save(output_image_file)
    logger.info(f"Saved to: {output_image_file!r}")

    output_json_file = os.path.join(output_dir, os.path.basename(json_file))
    json_data["imageData"] = None
    json_data["imagePath"] = os.path.relpath(output_image_file, output_dir)
    with open(output_json_file, "w") as f:
        json.dump(json_data, f, indent=2)
    logger.info(f"Saved to: {output_json_file!r}")


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
def extract_image(file_or_dir) -> None:
    """Extract image from a JSON file.

    Pass a JSON file or directory to extract from.

    Examples:

     \b
     $ labelmetk extract-image examples/small_dataset/2011_000003.json
     $ labelmetk extract-image examples/small_dataset/

    """
    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )
    for json_file in json_files:
        _extract_image(json_file=json_file, output_dir=output_dir)
