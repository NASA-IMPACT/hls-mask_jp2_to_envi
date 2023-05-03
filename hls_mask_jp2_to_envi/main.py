from pathlib import Path

import typer

from .safe import translate_bands

app = typer.Typer()


@app.command()
def main(
    input_dir: Path = typer.Option(
        ...,
        "--input-dir",
        help="Input directory containing QI_DATA sub-directory containing JPEG2000 files",
        file_okay=False,
        dir_okay=True,
        exists=True,
        readable=True,
        resolve_path=True,
    ),
    output_dir: Path = typer.Option(
        ...,
        "--output-dir",
        help="Output directory for writing ENVI files",
        file_okay=False,
        dir_okay=True,
        exists=False,
        writable=True,
        resolve_path=True,
    ),
):
    output_dir.mkdir(parents=True, exist_ok=True)
    print(bool(translate_bands(input_dir, output_dir)))


if __name__ == "__main__":
    app()
