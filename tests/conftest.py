from pathlib import Path

import pytest
from PIL import Image


@pytest.fixture
def image_file(tmp_path: Path) -> Path:
    path = tmp_path / "input.jpg"
    Image.new("RGB", (100, 50), (20, 40, 60)).save(path)
    return path


@pytest.fixture
def input_dir(tmp_path: Path) -> Path:
    directory = tmp_path / "images"
    directory.mkdir()
    Image.new("RGB", (100, 50), (20, 40, 60)).save(directory / "wide.jpg")
    Image.new("RGB", (40, 80), (60, 40, 20)).save(directory / "tall.png")
    (directory / "note.txt").write_text("not an image", encoding="utf-8")
    return directory
