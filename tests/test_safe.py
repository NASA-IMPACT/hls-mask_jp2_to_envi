from pathlib import Path
from shutil import copy
from tempfile import TemporaryDirectory

import rasterio

from hls_mask_jp2_to_envi import translate_bands
from hls_mask_jp2_to_envi.safe import _BANDS


def test_translate_bands_missing_qi_data_dir():
    with TemporaryDirectory() as output_dir:
        output_path = Path(output_dir)
        assert not translate_bands(output_path, output_path)


def test_translate_bands_missing_bands(input_path: Path):
    with TemporaryDirectory() as output_dir:
        output_path = Path(output_dir)
        copy(input_path / "QI_DATA" / "MSK_QUALIT_B01.jp2", output_path / "QI_DATA")
        assert not translate_bands(output_path, output_path)


def test_translate_bands_success(input_path: Path, output_path: Path):
    n_bands = len(_BANDS)
    path_pairs = translate_bands(input_path, output_path)

    assert len(path_pairs) == n_bands

    for jp2_path, envi_path in path_pairs:
        with rasterio.open(jp2_path) as jp2:
            jp2_profile = jp2.profile
        with rasterio.open(envi_path) as envi:
            envi_profile = envi.profile

        assert jp2_profile["driver"] == "JP2OpenJPEG"
        assert envi_profile["driver"] == "ENVI"
