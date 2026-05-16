"""Custom type definitions."""

from enum import StrEnum


class ResizeMode(StrEnum):
    """Supported resize modes."""

    STRETCH = "stretch"
    KEEP = "keep"
    CROP = "crop"
    PAD = "pad"
