import json
import os
from typing import Dict
from typing import List
from typing import Optional

import click
import imgviz
import PIL.Image
from loguru import logger

from .. import _browsers
from .. import _json
from .. import _labelme
from .. import _migrations
from .. import _paths


def _json_to_visualization(
    json_file: str,
    output_dir: str,
    exclude_labels: Optional[List[str]] = None,
) -> str:
    if exclude_labels is None:
        exclude_labels = []

    with open(json_file, "r") as f:
        json_data: Dict = json.load(f)
    _migrations.migrate_json_data(json_data)

    image: PIL.Image.Image
    if json_data["imageData"] is None:
        image_path = os.path.join(os.path.dirname(json_file), json_data["imagePath"])
        image = PIL.Image.open(image_path)
    else:
        image = PIL.Image.fromarray(
            _json.image_b64data_to_ndarray(json_data["imageData"])
        )

    num_groups = 0
    annotated_group_id_to_group_id: Dict[int, int] = {}
    colormap = imgviz.label_colormap()
    for shape in json_data["shapes"]:
        if shape["label"] in exclude_labels:
            continue

        if shape["group_id"] is not None:
            if shape["group_id"] in annotated_group_id_to_group_id:
                group_id = annotated_group_id_to_group_id[shape["group_id"]]
                draw_label = False
            annotated_group_id_to_group_id[shape["group_id"]] = group_id
        else:
            group_id = num_groups
            num_groups += 1
            draw_label = True

        shape = _labelme.Shape(
            type=shape["shape_type"],
            points=shape["points"],
            label=shape["label"],
        )

        color = tuple(colormap[group_id + 1])
        _labelme.draw_shape_(
            image=image,
            shape=shape,
            line_color=color,
            draw_points=True,
            point_fill_color=color,
            point_line_color=color,
            draw_label=draw_label,
        )

    output_dir = os.path.join(
        output_dir, os.path.splitext(os.path.basename(json_file))[0]
    )
    os.makedirs(output_dir, exist_ok=True)

    output_file = os.path.join(output_dir, "visualization.png")
    image.save(output_file)
    logger.info(f"Saved to: {output_file!r}")

    return output_file


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--exclude-labels",
    type=str,
    multiple=True,
    help="labels to exclude",
    default=None,
)
@click.option(
    "--browse",
    "-b",
    is_flag=True,
    help="browse the output files",
)
def json_to_visualization(file_or_dir, exclude_labels, browse: bool):
    """Convert a Labelme JSON file to a visualization.

    Pass a JSON file or directory to convert.

    Examples:

     \b
     $ labelmetk json-to-visualization examples/small_dataset/2011_000003.json
     $ labelmetk json-to-visualization examples/small_dataset/

    """
    json_files: List[str]
    output_dir: str
    json_files, output_dir = _paths.get_json_files_and_output_dir(
        file_or_dir=file_or_dir
    )

    json_file_to_output_files: Dict[str, List[str]] = {}
    for json_file in json_files:
        json_file_to_output_files[json_file] = [
            _json_to_visualization(
                json_file=json_file,
                output_dir=output_dir,
                exclude_labels=exclude_labels,
            )
        ]

    if browse and json_file_to_output_files:
        _browsers.browse_images(
            image_paths_per_group=json_file_to_output_files,
            prefix="json-to-visualization-",
        )
