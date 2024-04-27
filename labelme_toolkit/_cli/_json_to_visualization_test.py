import glob
import os.path as osp
import subprocess

import numpy as np
import PIL.Image

from .._testing import small_dataset  # noqa


def test_json_to_visualization(small_dataset):  # noqa
    subprocess.check_call(["labelmetk", "json-to-visualization", small_dataset])

    assert osp.isdir(osp.join(small_dataset + ".export"))
    visualization_files = glob.glob(
        osp.join(small_dataset + ".export", "*/visualization.jpg")
    )
    assert len(visualization_files) == 3

    for visualization_file in visualization_files:
        visualization = np.asarray(PIL.Image.open(visualization_file))
        assert visualization.dtype == np.uint8
        assert visualization.ndim == 3
