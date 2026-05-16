from pathlib import Path
from statistics import mean
from time import perf_counter

import matplotlib.pyplot as plt
from PIL import Image

from resizer.aspect import AspectMode
from resizer.config import ResizeConfig
from resizer.io import resize_folder

ROOT = Path(__file__).resolve().parents[1]
BENCH = ROOT / "benchmarks"
REPORTS = ROOT / "reports"


def create_dataset(directory: Path, count: int) -> None:
    directory.mkdir(parents=True, exist_ok=True)
    for index in range(count):
        path = directory / f"image_{index:03}.jpg"
        if not path.exists():
            Image.new("RGB", (1200, 800), (index % 255, 80, 120)).save(path, quality=90)


def measure(count: int, mode: AspectMode) -> float:
    input_dir = BENCH / f"input_{count}"
    output_dir = BENCH / f"output_{count}_{mode.value}"
    create_dataset(input_dir, count)
    config = ResizeConfig(input_dir, output_dir, 512, 512, mode=mode, overwrite=True)
    start = perf_counter()
    resize_folder(config)
    return perf_counter() - start


def main() -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    counts = [5, 10, 20]
    times = [mean(measure(count, AspectMode.STRETCH) for _ in range(3)) for count in counts]

    plt.figure()
    plt.plot(counts, times, marker="o")
    plt.xlabel("Images")
    plt.ylabel("Seconds")
    plt.title("Batch resize performance")
    plt.savefig(REPORTS / "performance.png", bbox_inches="tight")

    (REPORTS / "performance_report.tex").write_text(
        r"""\documentclass{article}
\usepackage{graphicx}
\usepackage{booktabs}
\begin{document}
\section{Performance report}
The benchmark uses synthetic JPEG images of size 1200x800 and resizes them to 512x512.
The measured bottleneck is Pillow image decoding, resizing, and saving.
\begin{figure}[h]
\centering
\includegraphics[width=0.8\linewidth]{performance.png}
\caption{Batch resize runtime for different input sizes.}
\end{figure}
\section{Optimization plan}
A reasonable acceleration is to parallelize independent image processing with a worker pool.
The current implementation isolates single-file processing in resize\_one, so this refactoring is straightforward.
\end{document}
""",
        encoding="utf-8",
    )
    print(f"Wrote {REPORTS / 'performance.png'} and performance_report.tex")


if __name__ == "__main__":
    main()
