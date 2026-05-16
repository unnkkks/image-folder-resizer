# Performance report

The main bottleneck is image decoding/resizing/saving in Pillow. The project contains `scripts/profile_resize.py`, which creates a synthetic dataset, runs batch resizing, and writes a chart to `reports/performance.png`.

Run:

```bash
uv run poe profile
```

The generated LaTeX report is stored in `reports/performance_report.tex`.

## Possible optimization

The baseline implementation processes images sequentially. A practical acceleration is parallel processing with `concurrent.futures.ProcessPoolExecutor` or `ThreadPoolExecutor`. Pillow releases the GIL in many native image operations, so threaded processing can improve throughput for IO-heavy batches. The current code is intentionally simple, but `resize_one` is already isolated enough to be mapped over a pool.
