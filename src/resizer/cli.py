"""Command-line interface for image-folder-resizer."""

from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import click

from resizer.aspect import AspectMode
from resizer.config import ResizeConfig
from resizer.io import resize_folder


def package_version() -> str:
    """Return installed package version."""
    try:
        return version("image-folder-resizer")
    except PackageNotFoundError:
        return "0.0.0"


def parse_rgb(value: str) -> tuple[int, int, int]:
    """Parse an RGB value written as R,G,B."""
    try:
        items = tuple(int(part.strip()) for part in value.split(","))
    except ValueError as exc:
        msg = "background must be R,G,B, for example 255,255,255"
        raise click.BadParameter(msg) from exc
    if len(items) != 3 or any(item < 0 or item > 255 for item in items):
        msg = "background must contain three integers from 0 to 255"
        raise click.BadParameter(msg)
    return items


@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.version_option(package_version())
@click.argument("input_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.argument("output_dir", type=click.Path(file_okay=False, path_type=Path))
@click.option("-w", "--width", required=True, type=click.IntRange(min=1), help="Target width in pixels.")
@click.option("-hgt", "--height", required=True, type=click.IntRange(min=1), help="Target height in pixels.")
@click.option(
    "-m",
    "--mode",
    type=click.Choice([item.value for item in AspectMode]),
    default=AspectMode.STRETCH.value,
    show_default=True,
    help="Aspect-ratio strategy: stretch, fit, fill, or pad.",
)
@click.option("-r", "--recursive", is_flag=True, help="Process nested folders.")
@click.option("--overwrite", is_flag=True, help="Overwrite existing output files.")
@click.option("--quality", default=90, show_default=True, type=click.IntRange(1, 100), help="Output quality.")
@click.option("--format", "image_format", type=click.Choice(["jpeg", "png", "webp"]), help="Force output format.")
@click.option("--background", default="255,255,255", show_default=True, help="RGB color for pad mode.")
def main(
    input_dir: Path,
    output_dir: Path,
    width: int,
    height: int,
    mode: str,
    *,
    recursive: bool,
    overwrite: bool,
    quality: int,
    image_format: str | None,
    background: str,
) -> None:
    """Resize every supported image in INPUT_DIR and write results to OUTPUT_DIR."""
    config = ResizeConfig(
        input_dir=input_dir,
        output_dir=output_dir,
        width=width,
        height=height,
        mode=AspectMode(mode),
        recursive=recursive,
        overwrite=overwrite,
        quality=quality,
        image_format=image_format,
        background=parse_rgb(background),
    )
    processed = resize_folder(config)
    click.echo(f"Processed {len(processed)} image(s).")


if __name__ == "__main__":
    main()
