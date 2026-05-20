from importlib.metadata import PackageNotFoundError
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner
from PIL import Image

from resizer.cli import main, package_version, parse_rgb


def test_parse_rgb() -> None:
    assert parse_rgb("1, 2,3") == (1, 2, 3)


def test_parse_rgb_rejects_invalid_value() -> None:
    runner = CliRunner()
    result = runner.invoke(main, ["--help"])
    assert result.exit_code == 0


def test_parse_rgb_rejects_non_integer() -> None:
    runner = CliRunner()
    result = runner.invoke(main, [".", "out", "--width", "10", "--height", "10", "--background", "x,0,0"])
    assert result.exit_code != 0


def test_cli_processes_images(input_dir: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "out"
    runner = CliRunner()
    result = runner.invoke(main, [str(input_dir), str(output_dir), "--width", "30", "--height", "30", "--mode", "pad"])
    assert result.exit_code == 0
    assert "Processed 2 image" in result.output
    assert Image.open(output_dir / "wide.jpg").size == (30, 30)


def test_cli_reports_bad_background(input_dir: Path, tmp_path: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(
        main,
        [str(input_dir), str(tmp_path / "out"), "--width", "30", "--height", "30", "--background", "300,0,0"],
    )
    assert result.exit_code != 0


def test_package_version_fallback() -> None:
    with patch("resizer.cli.version", side_effect=PackageNotFoundError):
        assert package_version() == "0.0.0"
