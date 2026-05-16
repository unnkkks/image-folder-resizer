"""Profile image resizing performance and generate report assets."""

from __future__ import annotations

import shutil
import time
from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image
from resizer.core import resize_directory

from resizer.types import AspectMode

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / ".bench"
REPORTS = ROOT / "reports"


def create_dataset(directory: Path, count: int) -> None:
    """Create a synthetic image dataset for benchmarking."""
    directory.mkdir(parents=True, exist_ok=True)
    for index in range(count):
        image = Image.new(
            "RGB",
            (800 + index % 5, 600 + index % 7),
            color=(index % 255, 120, 180),
        )
        image.save(directory / f"image_{index}.jpg")


def measure(count: int, mode: AspectMode) -> float:
    """Measure resizing time for a generated dataset."""
    input_dir = BENCH / f"input_{count}"
    output_dir = BENCH / f"output_{count}_{mode.value}"

    if input_dir.exists():
        shutil.rmtree(input_dir)
    if output_dir.exists():
        shutil.rmtree(output_dir)

    create_dataset(input_dir, count)

    start = time.perf_counter()
    resize_directory(input_dir, output_dir, width=512, height=512, mode=mode)
    return time.perf_counter() - start


def main() -> None:
    """Run the benchmark and save a performance chart."""
    REPORTS.mkdir(parents=True, exist_ok=True)

    counts = [5, 10, 20]
    modes = [AspectMode.STRETCH, AspectMode.FIT]

    for mode in modes:
        timings = [measure(count, mode) for count in counts]
        plt.plot(counts, timings, marker="o", label=mode.value)

    plt.xlabel("Images")
    plt.ylabel("Seconds")
    plt.title("Resize performance")
    plt.legend()
    plt.savefig(REPORTS / "performance.png", dpi=150)


if __name__ == "__main__":
    main()
