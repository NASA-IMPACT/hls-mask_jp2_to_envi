import tempfile
from pathlib import Path

from typer.testing import CliRunner

from hls_mask_jp2_to_envi import app

runner = CliRunner(echo_stdin=True, mix_stderr=False)


def test_inputdir_missing_option():
    result = runner.invoke(app, [])

    assert result.exit_code != 0
    assert "input-dir" in result.stderr
    assert "Missing option" in result.stderr


def test_inputdir_missing_argument():
    result = runner.invoke(app, ["--input-dir"])

    assert result.exit_code != 0
    assert "input-dir" in result.stderr
    assert "requires an argument" in result.stderr


def test_inputdir_not_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        # We don't want to do anything here because we simply want a unique,
        # temporary directory to be created AND then deleted, but capture the
        # path of the directory in tmpdir, so we can use the name AFTER this
        # block, knowing that we have the name of a non-existent directory.
        pass

    result = runner.invoke(app, ["--input-dir", tmpdir])

    assert result.exit_code != 0
    assert "input-dir" in result.stderr
    assert "does not exist" in result.stderr


def test_inputdir_not_directory():
    result = runner.invoke(
        app,
        [
            "--input-dir",
            f"{Path(__file__).absolute()}",
        ],
    )

    assert result.exit_code != 0
    assert "input-dir" in result.stderr
    assert "is a file" in result.stderr


def test_outputdir_missing_option():
    result = runner.invoke(
        app,
        [
            "--input-dir",
            f"{Path(__file__).parent.absolute()}",
        ],
    )

    assert result.exit_code != 0
    assert "Missing option" in result.stderr
    assert "output-dir" in result.stderr


def test_outputdir_missing_argument():
    result = runner.invoke(
        app,
        [
            "--input-dir",
            f"{Path(__file__).parent.absolute()}",
            "--output-dir",
        ],
    )

    assert result.exit_code != 0
    assert "output-dir" in result.stderr
    assert "requires an argument" in result.stderr


def test_outputdir_not_exists():
    with tempfile.TemporaryDirectory() as tmpdir:
        # We don't want to do anything here because we simply want a unique,
        # temporary directory to be created AND then deleted, but capture the
        # path of the directory in tmpdir, so we can use the name AFTER this
        # block, knowing that we have the name of a non-existent directory.
        pass

    result = runner.invoke(
        app,
        [
            "--input-dir",
            f"{Path(__file__).parent.absolute()}",
            "--output-dir",
            tmpdir,
        ],
    )

    # It's okay to specify an output directory that does not exist.  It will be
    # created, in this case.
    assert result.exit_code == 0


def test_outputdir_not_directory():
    result = runner.invoke(
        app,
        [
            "--input-dir",
            f"{Path(__file__).parent.absolute()}",
            "--output-dir",
            f"{Path(__file__).absolute()}",
        ],
    )

    assert result.exit_code != 0
    assert "output-dir" in result.stderr
    assert "is a file" in result.stderr


def test_print_false_on_failure():
    with tempfile.TemporaryDirectory() as tmpdir:
        result = runner.invoke(
            app,
            [
                "--input-dir",
                tmpdir,
                "--output-dir",
                tmpdir,
            ],
        )

    # A "failure" still exits with a 0 exit code, but prints False to stdout to
    # indicate failure.
    assert result.exit_code == 0
    assert result.stdout == "False\n"
    assert result.stderr == ""


def test_print_true_on_success(input_path: Path, output_path: Path):
    result = runner.invoke(
        app,
        [
            "--input-dir",
            input_path,
            "--output-dir",
            output_path,
        ],
    )

    assert result.exit_code == 0
    assert result.stdout == "True\n"
