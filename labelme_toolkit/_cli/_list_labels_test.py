import subprocess

from .._testing import small_dataset  # noqa


def test_list_labels(small_dataset):  # noqa
    output = subprocess.check_output(
        ["labelmetk", "list-labels", small_dataset]
    ).decode()

    assert [line.strip() for line in output.splitlines()] == [
        "__ignore__",
        "bottle",
        "bus",
        "car",
        "chair",
        "person",
        "sofa",
    ]
