"""Batch image resizing with aspect-ratio strategies."""

from resizer.aspect import AspectMode
from resizer.config import ResizeConfig
from resizer.image_ops import resize_image
from resizer.io import resize_folder

__all__ = ["AspectMode", "ResizeConfig", "resize_folder", "resize_image"]
__version__ = "0.1.0"
