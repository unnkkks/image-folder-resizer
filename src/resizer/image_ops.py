"""Image resizing operations."""

from pathlib import Path

from PIL import Image, UnidentifiedImageError

from resizer.aspect import AspectMode, centered_crop_box, centered_paste_position, fill_size, fit_size
from resizer.exceptions import UnsupportedImageError


def open_image(path: Path) -> Image.Image:
    """Open an image from disk and return an RGB/RGBA-compatible copy."""
    try:
        with Image.open(path) as image:
            image.load()
            if image.mode in {"RGBA", "LA"}:
                return image.convert("RGBA")
            return image.convert("RGB")
    except (UnidentifiedImageError, OSError) as exc:
        msg = f"unsupported image file: {path}"
        raise UnsupportedImageError(msg) from exc


def resize_image(
    image: Image.Image,
    target_size: tuple[int, int],
    mode: AspectMode = AspectMode.STRETCH,
    *,
    background: tuple[int, int, int] = (255, 255, 255),
    resample: int = Image.Resampling.LANCZOS,
) -> Image.Image:
    """Resize an image using the selected aspect-ratio strategy."""
    if target_size[0] <= 0 or target_size[1] <= 0:
        msg = "target size values must be positive"
        raise ValueError(msg)

    match mode:
        case AspectMode.STRETCH:
            return image.resize(target_size, resample=resample)
        case AspectMode.FIT:
            return image.resize(fit_size(image.size, target_size), resample=resample)
        case AspectMode.FILL:
            resized = image.resize(fill_size(image.size, target_size), resample=resample)
            return resized.crop(centered_crop_box(resized.size, target_size))
        case AspectMode.PAD:
            resized = image.resize(fit_size(image.size, target_size), resample=resample)
            canvas = Image.new("RGB", target_size, background)
            paste_at = centered_paste_position(target_size, resized.size)
            if resized.mode == "RGBA":
                canvas.paste(resized, paste_at, resized)
            else:
                canvas.paste(resized, paste_at)
            return canvas

    msg = f"unsupported aspect mode: {mode}"
    raise ValueError(msg)
