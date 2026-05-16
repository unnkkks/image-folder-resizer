from pathlib import Path

import pytest

from resizer.config import ResizeConfig


def test_config_target_size(tmp_path: Path) -> None:
    config = ResizeConfig(tmp_path, tmp_path / "out", 10, 20)
    assert config.target_size == (10, 20)


def test_config_rejects_non_positive_size(tmp_path: Path) -> None:
    config = ResizeConfig(tmp_path, tmp_path / "out", 0, 20)
    with pytest.raises(ValueError):
        config.validate()


def test_config_rejects_bad_quality(tmp_path: Path) -> None:
    config = ResizeConfig(tmp_path, tmp_path / "out", 10, 20, quality=101)
    with pytest.raises(ValueError):
        config.validate()


def test_config_requires_existing_input(tmp_path: Path) -> None:
    config = ResizeConfig(tmp_path / "missing", tmp_path / "out", 10, 20)
    with pytest.raises(FileNotFoundError):
        config.validate()


def test_config_requires_directory(tmp_path: Path) -> None:
    file_path = tmp_path / "file.txt"
    file_path.write_text("x", encoding="utf-8")
    config = ResizeConfig(file_path, tmp_path / "out", 10, 20)
    with pytest.raises(NotADirectoryError):
        config.validate()
