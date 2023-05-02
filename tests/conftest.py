from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Iterable
from zipfile import ZipFile

import pytest


@pytest.fixture(scope="session")
def input_path() -> Iterable[Path]:
    """
    Yield input path containing QI_DATA subdirectory containing jp2 fixture files.

    Unzip test fixture zip file containing SAFE files, making only the jp2 files
    available during the test session, then cleanup the files at the end of the
    session.
    """
    id_ = "S2B_MSIL1C_20210617T100559_N7990_R022_T35VLJ_20211119T091141"
    zip_file = ZipFile(Path(__file__).parent / f"{id_}.zip")
    jp2_paths = [name for name in zip_file.namelist() if "/MSK_QUALIT_B" in name]

    with TemporaryDirectory() as tmpdir:
        # Extract only the jp2 files to save a bit of time during both
        # extraction and cleanup.
        zip_file.extractall(path=tmpdir, members=jp2_paths)

        # Yield path to the only sub-directory of the GRANULE sub-directory,
        # which is the input directory expected by translate_bands.
        yield next((Path(tmpdir) / f"{id_}.SAFE" / "GRANULE").iterdir())


@pytest.fixture(scope="session")
def output_path() -> Iterable[Path]:
    """Yield output path for writing ENVI files."""
    with TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)
