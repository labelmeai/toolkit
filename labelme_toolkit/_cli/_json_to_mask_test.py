import glob
import os.path as osp
import subprocess

import numpy as np
import PIL.Image

from .._testing import small_dataset  # noqa


def test_json_to_mask(small_dataset):  # noqa
    subprocess.check_call(["labelmetk", "json-to-mask", small_dataset])

    assert osp.isdir(osp.join(small_dataset + ".export"))
    mask_files = glob.glob(osp.join(small_dataset + ".export", "*/mask.png"))
    assert len(mask_files) == 3

    for mask_file in mask_files:
        mask = np.asarray(PIL.Image.open(mask_file))
        assert mask.dtype == np.uint8
        assert mask.ndim == 2
