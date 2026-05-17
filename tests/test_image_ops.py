from pathlib import Path

import pytest
from PIL import Image

from resizer.aspect import AspectMode
from resizer.exceptions import UnsupportedImageError
from resizer.image_ops import open_image, resize_image


def test_open_image_returns_rgb_copy(image_file: Path) -> None:
    image = open_image(image_file)
    assert image.size == (100, 50)
    assert image.mode == "RGB"


def test_open_image_rejects_text(tmp_path: Path) -> None:
    path = tmp_path / "bad.jpg"
    path.write_text("broken", encoding="utf-8")
    with pytest.raises(UnsupportedImageError):
        open_image(path)


def test_resize_stretch() -> None:
    image = Image.new("RGB", (100, 50))
    assert resize_image(image, (40, 40), AspectMode.STRETCH).size == (40, 40)


def test_resize_fit() -> None:
    image = Image.new("RGB", (100, 50))
    assert resize_image(image, (40, 40), AspectMode.FIT).size == (40, 20)


def test_resize_fill() -> None:
    image = Image.new("RGB", (100, 50))
    assert resize_image(image, (40, 40), AspectMode.FILL).size == (40, 40)


def test_resize_pad() -> None:
    image = Image.new("RGB", (100, 50))
    assert resize_image(image, (40, 40), AspectMode.PAD).size == (40, 40)


def test_resize_pad_rgba() -> None:
    image = Image.new("RGBA", (10, 10), (255, 0, 0, 128))
    assert resize_image(image, (20, 20), AspectMode.PAD).mode == "RGB"


def test_resize_requires_positive_target() -> None:
    image = Image.new("RGB", (100, 50))
    with pytest.raises(ValueError, match="positive"):
        resize_image(image, (0, 40))


def test_open_image_converts_rgba(tmp_path: Path) -> None:
    path = tmp_path / "alpha.png"
    Image.new("RGBA", (5, 5), (255, 0, 0, 128)).save(path)
    assert open_image(path).mode == "RGBA"


def test_resize_rejects_unknown_mode() -> None:
    image = Image.new("RGB", (10, 10))
    with pytest.raises(TypeError, match="unsupported"):
        resize_image(image, (5, 5), "unknown")  # type: ignore[arg-type]
