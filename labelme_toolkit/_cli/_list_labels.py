import json
from typing import List

import click

from .. import _paths


@click.command()
@click.argument("file_or_dir", type=click.Path(exists=True), required=True)
def list_labels(file_or_dir: str):
    """List unique labels in the JSON files.

    Pass a JSON file or directory to list unique labels from.

    Example:

     \b
     $ labelmetk list-labels examples/small_dataset/2011_000003.json
     $ labelmetk list-labels examples/small_dataset/

    """
    json_files: List[str]
    json_files, _ = _paths.get_json_files_and_output_dir(file_or_dir=file_or_dir)

    unique_labels: set = set()
    json_file: str
    for json_file in json_files:
        with open(json_file) as f:
            json_data = json.load(f)

        for json_shape in json_data["shapes"]:
            unique_labels.add(json_shape["label"])

    click.echo("\n".join(sorted(unique_labels)))
