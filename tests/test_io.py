from pathlib import Path
from unittest.mock import patch

import pytest
from PIL import Image

from resizer.aspect import AspectMode
from resizer.config import ResizeConfig
from resizer.exceptions import OutputExistsError
from resizer.io import iter_images, output_path_for, resize_folder, resize_one, save_image


def test_iter_images_ignores_non_images(input_dir: Path) -> None:
    names = [path.name for path in iter_images(input_dir)]
    assert names == ["tall.png", "wide.jpg"]


def test_iter_images_recursive(input_dir: Path) -> None:
    nested = input_dir / "nested"
    nested.mkdir()
    Image.new("RGB", (10, 10)).save(nested / "inside.webp")
    names = [path.name for path in iter_images(input_dir, recursive=True)]
    assert set(names) == {"tall.png", "wide.jpg", "inside.webp"}


def test_output_path_for_keeps_nested_structure(input_dir: Path, tmp_path: Path) -> None:
    nested = input_dir / "nested"
    nested.mkdir()
    image = nested / "inside.jpg"
    image.write_bytes(b"x")
    config = ResizeConfig(input_dir, tmp_path / "out", 20, 20, recursive=True, image_format="png")
    assert output_path_for(image, config) == tmp_path / "out" / "nested" / "inside.png"


def test_resize_folder_processes_supported_files(input_dir: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    config = ResizeConfig(input_dir, output_dir, 20, 20, AspectMode.STRETCH)
    processed = resize_folder(config)
    assert len(processed) == 2
    assert all(path.exists() for path in processed)
    assert Image.open(output_dir / "wide.jpg").size == (20, 20)


def test_resize_one_blocks_existing_output(image_file: Path, tmp_path: Path) -> None:
    output = tmp_path / "out.jpg"
    output.write_bytes(b"old")
    config = ResizeConfig(image_file.parent, tmp_path, 20, 20)
    with pytest.raises(OutputExistsError):
        resize_one(image_file, output, config)


def test_save_image_forced_format(tmp_path: Path) -> None:
    image = Image.new("RGB", (10, 10))
    output = tmp_path / "image.webp"
    save_image(image, output, quality=80, image_format="webp")
    assert output.exists()


def test_resize_folder_skips_corrupted_supported_file(tmp_path: Path) -> None:
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    (input_dir / "broken.jpg").write_text("broken", encoding="utf-8")
    config = ResizeConfig(input_dir, tmp_path / "out", 20, 20)
    assert resize_folder(config) == []


def test_resize_one_uses_mocked_io(image_file: Path, tmp_path: Path) -> None:
    image = Image.new("RGB", (10, 10))
    output = tmp_path / "out.jpg"
    config = ResizeConfig(image_file.parent, tmp_path, 5, 5, overwrite=True)
    with patch("resizer.io.open_image", return_value=image) as mocked_open, patch("resizer.io.save_image") as mocked_save:
        assert resize_one(image_file, output, config) == output
    mocked_open.assert_called_once_with(image_file)
    mocked_save.assert_called_once()
