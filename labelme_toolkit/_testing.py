import os.path as osp
import shutil
import tempfile
import zipfile

import pytest

here = osp.dirname(osp.abspath(__file__))


@pytest.fixture
def small_dataset():
    tmp_dir = tempfile.mkdtemp()

    shutil.copy(
        osp.join(here, "_data/small_dataset.zip"),
        osp.join(tmp_dir, "small_dataset.zip"),
    )
    with zipfile.ZipFile(osp.join(tmp_dir, "small_dataset.zip"), "r") as f:
        f.extractall(tmp_dir)

    yield osp.join(tmp_dir, "small_dataset")

    shutil.rmtree(tmp_dir)
