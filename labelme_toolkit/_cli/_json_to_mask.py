import json
import os
from typing import Dict
from typing import List
from typing import Optional

import click
import numpy as np
import PIL.Image
from loguru import logger

from .. import _browsers
from .. import _labelme
from .. import _migrations
from .. import _paths


def _json_to_mask(
    json_file: str,
    output_dir: str,
    include_labels: Optional[List[str]] = None,
    exclude_labels: Optional[List[str]] = None,
) -> str:
    if include_labels and exclude_labels:
        raise ValueError("include_labels and exclude_labels must not be used together")

    with open(json_file) as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data=json_data)

    mask = np.zeros((json_data["imageHeight"], json_data["imageWidth"]), dtype=bool)
    for i, shape in enumerate(json_data["shapes"]):
        shape = _labelme.Shape(
            type=shape["shape_type"],
            points=shape["points"],
            label=shape["label"],
        )

        if include_labels is not None and shape.label not in include_labels:
            logger.info(
                f"Ignoring shape[{i}].label={shape.label!r} in {json_file!r} by "
                f"include_labels={include_labels!r}"
            )
            continue
        if exclude_labels is not None and shape.label in exclude_labels:
            logger.info(
                f"Ignoring shape[{i}].label={shape.label!r} in {json_file!r} by "
                f"exclude_labels={exclude_labels!r}"
            )
            continue

        mask_i = _labelme.shape_to_mask(
            shape=shape,
            image_height=json_data["imageHeight"],
            image_width=json_data["imageWidth"],
        )
        mask |= mask_i

    output_dir = os.path.join(
        output_dir, os.path.splitext(os.path.basename(json_file))[0]
    )
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "mask.png")
    PIL.Image.fromarray(mask.astype("uint8") * 255).save(output_file)
    logger.info(f"Saved to: {output_file!r}")

    return output_file


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--include-labels",
    type=str,
    multiple=True,
    help="labels to include (cannot be used with --exclude-labels)",
    default=None,
)
@click.option(
    "--exclude-labels",
    type=str,
    multiple=True,
    help="labels to exclude (cannot be used with --include-labels)",
    default=None,
)
@click.option(
    "--browse",
    "-b",
    is_flag=True,
    help="browse the output files",
)
def json_to_mask(file_or_dir, include_labels, exclude_labels, browse: bool):
    """Convert a Labelme JSON file to a mask.

    Pass a JSON file or directory to convert.

    Examples:

     \b
     $ labelmetk json-to-mask examples/small_dataset/2011_000003.json
     $ labelmetk json-to-mask examples/small_dataset/

    """
    if include_labels and exclude_labels:
        raise click.BadOptionUsage(
            option_name="include-labels",
            message="--include-labels cannot be used with --exclude-labels",
        )

    # Click does not respect the default=None for multiple=True
    if not include_labels:
        include_labels = None
    if not exclude_labels:
        exclude_labels = None

    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )

    json_file_to_output_files: Dict[str, List[str]] = {}
    json_file: str
    for json_file in json_files:
        json_file_to_output_files[json_file] = [
            _json_to_mask(
                json_file=json_file,
                output_dir=output_dir,
                include_labels=include_labels,
                exclude_labels=exclude_labels,
            )
        ]

    if browse and json_file_to_output_files:
        _browsers.browse_images(
            image_paths_per_group=json_file_to_output_files, prefix="json-to-mask-"
        )
