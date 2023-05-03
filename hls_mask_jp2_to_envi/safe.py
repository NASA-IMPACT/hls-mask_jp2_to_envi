import sys
from pathlib import Path
from typing import Sequence, Tuple

from rasterio.shutil import copy
from typing_extensions import Final

_BANDS: Final = "01 02 03 04 05 06 07 08 8A 09 10 11 12".split()


def translate_bands(input_dir: Path, output_dir: Path) -> Sequence[Tuple[Path, Path]]:
    """
    Translate all JPEG2000 files like ``<input_dir>/QI_DATA/MSK_QUALIT_B*.jp2``
    to ENVI files like ``<output_dir>/MSK_QUALIT_B*.envi``.

    Return sequence of pairs of jp2 and envi file paths if there is a jp2 file
    for every band in 01, 02, 03, 04, 05, 06, 07, 08, 8A, 09, 10, 11, 12, and
    all are translated to ENVI files; otherwise an empty sequence.
    """
    jp2_envi_paths = [
        (jp2_path, (output_dir / jp2_path.stem).with_suffix(".envi"))
        for jp2_path in (input_dir / "QI_DATA").glob("MSK_QUALIT_B*.jp2")
        if jp2_path.stem[-2:] in _BANDS
    ]

    if len(jp2_envi_paths) < len(_BANDS):
        return []

    for jp2_path, envi_path in jp2_envi_paths:
        print(f"Translating {jp2_path} to {envi_path}", file=sys.stderr)
        if not envi_path.exists():
            copy(jp2_path, envi_path, driver="ENVI", interleave="bip")

    return jp2_envi_paths
