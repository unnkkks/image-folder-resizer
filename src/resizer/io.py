"""Filesystem IO for batch image processing."""

from collections.abc import Iterator
from pathlib import Path

from PIL import Image

from resizer.config import ResizeConfig
from resizer.exceptions import OutputExistsError, UnsupportedImageError
from resizer.image_ops import open_image, resize_image

SUPPORTED_EXTENSIONS = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}


def iter_images(directory: Path, *, recursive: bool = False) -> Iterator[Path]:
    """Yield supported image paths from a directory."""
    pattern = "**/*" if recursive else "*"
    for path in sorted(directory.glob(pattern)):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def output_path_for(input_path: Path, config: ResizeConfig) -> Path:
    """Return output path while preserving relative structure for recursive mode."""
    relative = input_path.relative_to(config.input_dir) if config.recursive else Path(input_path.name)
    suffix = f".{config.image_format.lower()}" if config.image_format else input_path.suffix
    return config.output_dir / relative.with_suffix(suffix)


def save_image(image: Image.Image, path: Path, *, quality: int, image_format: str | None) -> None:
    """Save processed image to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fmt = image_format.upper() if image_format else None
    if path.suffix.lower() in {".jpg", ".jpeg"} or fmt == "JPEG":
        image = image.convert("RGB")
    image.save(path, format=fmt, quality=quality)


def resize_one(input_path: Path, output_path: Path, config: ResizeConfig) -> Path:
    """Resize one image and save it to output_path."""
    if output_path.exists() and not config.overwrite:
        msg = f"output file already exists: {output_path}"
        raise OutputExistsError(msg)
    image = open_image(input_path)
    resized = resize_image(
        image,
        config.target_size,
        config.mode,
        background=config.background,
        resample=config.resample,
    )
    save_image(resized, output_path, quality=config.quality, image_format=config.image_format)
    return output_path


def resize_folder(config: ResizeConfig) -> list[Path]:
    """Resize all supported images in the configured folder."""
    config.validate()
    config.output_dir.mkdir(parents=True, exist_ok=True)
    processed: list[Path] = []
    for input_path in iter_images(config.input_dir, recursive=config.recursive):
        output_path = output_path_for(input_path, config)
        try:
            processed.append(resize_one(input_path, output_path, config))
        except UnsupportedImageError:
            continue
    return processed
