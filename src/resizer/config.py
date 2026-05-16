"""Configuration model for batch resizing."""

from dataclasses import dataclass
from pathlib import Path

from PIL import Image

from resizer.aspect import AspectMode


@dataclass(frozen=True, slots=True)
class ResizeConfig:
    """User options for processing a folder of images."""

    input_dir: Path
    output_dir: Path
    width: int
    height: int
    mode: AspectMode = AspectMode.STRETCH
    recursive: bool = False
    overwrite: bool = False
    quality: int = 90
    background: tuple[int, int, int] = (255, 255, 255)
    image_format: str | None = None
    resample: int = Image.Resampling.LANCZOS

    @property
    def target_size(self) -> tuple[int, int]:
        """Return requested target size."""
        return self.width, self.height

    def validate(self) -> None:
        """Validate configuration values before processing."""
        if self.width <= 0 or self.height <= 0:
            msg = "width and height must be positive integers"
            raise ValueError(msg)
        if not 1 <= self.quality <= 100:
            msg = "quality must be in range 1..100"
            raise ValueError(msg)
        if not self.input_dir.exists():
            msg = f"input directory does not exist: {self.input_dir}"
            raise FileNotFoundError(msg)
        if not self.input_dir.is_dir():
            msg = f"input path is not a directory: {self.input_dir}"
            raise NotADirectoryError(msg)
