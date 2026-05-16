"""Aspect-ratio calculation helpers."""

from enum import StrEnum
from math import ceil


class AspectMode(StrEnum):
    """Available image resize strategies."""

    STRETCH = "stretch"
    FIT = "fit"
    FILL = "fill"
    PAD = "pad"


def fit_size(source: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    """Return the largest size fitting source into target while preserving aspect ratio."""
    src_width, src_height = source
    dst_width, dst_height = target
    scale = min(dst_width / src_width, dst_height / src_height)
    return max(1, round(src_width * scale)), max(1, round(src_height * scale))


def fill_size(source: tuple[int, int], target: tuple[int, int]) -> tuple[int, int]:
    """Return the smallest size covering target while preserving aspect ratio."""
    src_width, src_height = source
    dst_width, dst_height = target
    scale = max(dst_width / src_width, dst_height / src_height)
    return max(1, ceil(src_width * scale)), max(1, ceil(src_height * scale))


def centered_crop_box(size: tuple[int, int], target: tuple[int, int]) -> tuple[int, int, int, int]:
    """Return a centered crop box for PIL.Image.crop."""
    width, height = size
    target_width, target_height = target
    left = max(0, (width - target_width) // 2)
    top = max(0, (height - target_height) // 2)
    return left, top, left + target_width, top + target_height


def centered_paste_position(canvas: tuple[int, int], image: tuple[int, int]) -> tuple[int, int]:
    """Return the position for centering an image on a canvas."""
    canvas_width, canvas_height = canvas
    image_width, image_height = image
    return (canvas_width - image_width) // 2, (canvas_height - image_height) // 2
