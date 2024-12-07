import json
import os
from typing import Dict
from typing import List

import click
import numpy as np
import osam.apis
import osam.types
import PIL.Image
from loguru import logger

from .. import _labelme
from .. import _paths


def _ai_annotate_rectangles(
    image_file: str,
    output_dir: str,
    model: str,
    texts: List[str],
    iou_threshold: float,
    score_threshold: float,
    max_annotations: int,
) -> None:
    image: np.ndarray = np.asarray(PIL.Image.open(image_file))

    response: osam.types.GenerateResponse = osam.apis.generate(
        request=osam.types.GenerateRequest(
            model=model,
            image=image,
            prompt=osam.types.Prompt(
                texts=texts,
                iou_threshold=iou_threshold,
                score_threshold=score_threshold,
                max_annotations=max_annotations,
            ),
        ),
    )

    shapes: List[Dict] = []
    for annotation in response.annotations:
        shape: _labelme.Shape = _labelme.Shape(
            type="rectangle",
            points=np.array(
                [
                    [annotation.bounding_box.xmin, annotation.bounding_box.ymin],
                    [annotation.bounding_box.xmax, annotation.bounding_box.ymax],
                ],
                dtype=np.float32,
            ),
            label=annotation.text,
        )
        shape_dict: Dict = shape.to_json()
        shape_dict["description"] = json.dumps(annotation.dict())
        shapes.append(shape_dict)

    os.makedirs(output_dir, exist_ok=True)
    #
    output_json_file: str = os.path.join(
        output_dir, os.path.splitext(os.path.basename(image_file))[0] + ".json"
    )
    with open(output_json_file, "w") as f:
        json.dump(
            {
                "flags": {},
                "shapes": shapes,
                "imagePath": os.path.basename(image_file),
                "imageData": None,
                "imageHeight": image.shape[0],
                "imageWidth": image.shape[1],
            },
            f,
            indent=2,
        )
    logger.info(f"{image_file!r} - Saved to {output_json_file!r}")

    output_image_file: str = os.path.join(output_dir, os.path.basename(image_file))
    PIL.Image.fromarray(image).save(output_image_file)
    logger.info(f"{image_file!r} - Saved to {output_image_file!r}")


def _comma_separated_text(value: str) -> List[str]:
    return value.split(",")


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
@click.option(
    "--model",
    type=str,
    default="yoloworld",
    show_default=True,
    help="Model. (yoloworld: GPLv3)",
)
@click.option(
    "--texts",
    type=_comma_separated_text,
    help="Comma separated texts to annotate (e.g., 'dog,cat').",
    required=True,
)
@click.option(
    "--iou-threshold",
    type=float,
    default=0.5,
    show_default=True,
    help="IOU threshold.",
)
@click.option(
    "--score-threshold",
    type=float,
    default=0.1,
    show_default=True,
    help="Score threshold.",
)
@click.option(
    "--max-annotations",
    type=int,
    default=100,
    show_default=True,
    help="Max annotations.",
)
def ai_annotate_rectangles(file_or_dir: str, **kwargs) -> None:
    """Annotate rectangle from text by AI.

    Pass a image file or a directory to annotate.

    Examples:

     \b
     $ labelmetk ai-annotate-rectangles examples/small_dataset/2011_000003.jpg --texts person,hat
     $ labelmetk ai-annotate-rectangles examples/small_dataset/ --texts person,hat

    """  # noqa: E501
    image_files: List[str]
    output_dir: str
    image_files, output_dir = _paths.get_files_and_output_dir(
        file_or_dir=file_or_dir, pattern=r".*\.(jpg|jpeg|png)$"
    )

    for image_file in image_files:
        _ai_annotate_rectangles(
            image_file=image_file,
            output_dir=output_dir,
            **kwargs,
        )
