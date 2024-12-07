import dataclasses
from typing import Optional
from typing import Tuple
from typing import Union

import numpy as np
import PIL.Image
import PIL.ImageDraw

from . import _json


@dataclasses.dataclass
class Shape:
    type: str
    points: np.ndarray
    label: str
    group_id: Optional[int] = None
    mask: Optional[np.ndarray] = None

    def __post_init__(self):
        self.points = np.asarray(self.points)

        if self.type not in ["circle", "rectangle", "polygon", "mask"]:
            raise ValueError(f"Unsupported shape type={self.type!r}")
        if not (self.points.ndim == 2 and self.points.shape[1] == 2):
            raise ValueError(f"Invalid shape points.shape={self.points.shape!r}")
        if self.type in ["circle", "rectangle"] and self.points.shape != (2, 2):
            raise ValueError(
                f"Invalid shape points.shape={self.points.shape!r} for "
                f"type={self.type!r}"
            )
        if self.type == "mask":
            if self.mask is None:
                raise ValueError(f"shape.type={self.type!r} requires mask")
            if self.mask.ndim != 2:
                raise ValueError(f"expected mask.ndim=2, but got {self.mask.ndim}")
            if self.mask.dtype != bool:
                raise ValueError(f"expected mask.dtype=bool, but got {self.mask.dtype}")
            if self.points.size != 4:
                raise ValueError(
                    f"expected shape.points.size=4, but got {self.points.size}"
                )

            mask_height, mask_width = self.mask.shape
            (xmin, ymin), (xmax, ymax) = self.points
            if xmax - xmin + 1 != mask_width or ymax - ymin + 1 != mask_height:
                raise ValueError(
                    f"shape.points={self.points!r} does not match "
                    f"mask.shape={self.mask.shape!r}"
                )

    def to_json(self):
        return {
            "label": self.label,
            "points": self.points.tolist(),
            "shape_type": self.type,
            "mask": None
            if self.mask is None
            else _json.image_ndarray_to_b64data(ndarray=self.mask),
            "group_id": self.group_id,
        }


def shape_to_mask(shape: Shape, image_height: int, image_width: int) -> np.ndarray:
    mask: np.ndarray = np.zeros((image_height, image_width), dtype=np.uint8)

    mask_pil: PIL.Image.Image = PIL.Image.fromarray(mask)
    draw_shape_(image=mask_pil, shape=shape, fill_color=1, line_color=1)
    mask = np.asarray(mask_pil, dtype=bool)

    return mask


def draw_shape_(
    image: PIL.Image.Image,
    shape: Shape,
    fill_color: Union[None, int, Tuple[int, int, int]] = None,
    line_color: Union[None, int, Tuple[int, int, int]] = None,
    draw_points=False,
    point_fill_color: Union[None, int, Tuple[int, int, int]] = None,
    point_line_color: Union[None, int, Tuple[int, int, int]] = None,
    draw_label=False,
):
    draw = PIL.ImageDraw.Draw(image)

    points = tuple([tuple(point) for point in shape.points])

    line_width = max(1, min(image.size) // 150)
    if shape.type == "circle":
        cx: float
        cy: float
        px: float
        py: float
        (cx, cy), (px, py) = points  # type: ignore
        r = np.sqrt((cx - px) ** 2 + (cy - py) ** 2)
        draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=fill_color,
            outline=line_color,
            width=line_width,
        )
    elif shape.type == "rectangle":
        draw.rectangle(
            xy=points,  # type: ignore
            fill=fill_color,
            outline=line_color,
            width=line_width,
        )
    elif shape.type == "polygon":
        draw.polygon(xy=points, fill=fill_color, outline=line_color, width=line_width)
    elif shape.type == "mask":
        assert shape.mask is not None
        mask_height, mask_width = shape.mask.shape
        (xmin, ymin), (xmax, ymax) = points
        mask = PIL.Image.fromarray(shape.mask)
        mask = mask.resize(
            (xmax - xmin + 1, ymax - ymin + 1), resample=PIL.Image.NEAREST
        )
        image.paste(mask, (xmin, ymin))
    else:
        raise ValueError(f"Cannot draw shape type={shape.type!r}")

    if draw_points:
        point_radius = max(1, min(image.size) // 150)
        for point in points:
            cx, cy = point
            draw.ellipse(
                [
                    cx - point_radius,
                    cy - point_radius,
                    cx + point_radius,
                    cy + point_radius,
                ],
                fill=point_fill_color,
                outline=point_line_color,
            )

    if draw_label:
        font_size = min(image.size) // 30
        bbox = draw.textbbox(xy=points[0], text=shape.label, font_size=font_size)
        pad = 1
        draw.rectangle(
            [bbox[0] - pad, bbox[1] - pad, bbox[2] + pad, bbox[3] + pad],  # type: ignore
            fill=(255, 255, 255),
        )
        draw.text(xy=points[0], text=shape.label, fill=line_color, font_size=font_size)
