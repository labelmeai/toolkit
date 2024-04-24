from typing import Dict


def migrate_json_data(json_data: Dict) -> None:
    for shape in json_data["shapes"]:
        if "shape_type" not in shape:
            shape["shape_type"] = "polygon"

        if "group_id" not in shape:
            shape["group_id"] = None
