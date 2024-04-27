import glob
import json
import os.path as osp
import subprocess

import numpy as np
import PIL.Image

from .._testing import small_dataset  # noqa


def test_extract_image(small_dataset):  # noqa
    subprocess.check_call(["labelmetk", "extract-image", small_dataset])

    assert osp.isdir(osp.join(small_dataset + ".export"))
    json_files = glob.glob(osp.join(small_dataset + ".export", "*.json"))
    assert len(json_files) == 3

    for json_file in json_files:
        with open(json_file) as f:
            json_data = json.load(f)
        assert json_data["imageData"] is None

        image_file = json_file.replace(".json", ".jpg")
        assert osp.isfile(image_file)

        assert json_data["imagePath"] == osp.basename(image_file)
        image = np.asarray(PIL.Image.open(image_file))
        assert image.dtype == np.uint8
        assert image.ndim == 3
        assert json_data["imageHeight"] == image.shape[0]
        assert json_data["imageWidth"] == image.shape[1]
