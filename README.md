# image-folder-resizer

[![Tests](https://github.com/unnkkks/image-folder-resizer/actions/workflows/ci.yml/badge.svg)](https://github.com/unnkkks/image-folder-resizer/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen)](./coverage.xml)

Batch CLI utility for resizing every supported image in a folder.

## Features

- `stretch`: resize exactly to requested width and height, allowing stretching/compression.
- `fit`: preserve aspect ratio and fit inside the target box.
- `fill`: preserve aspect ratio, cover the target box, then crop center.
- `pad`: preserve aspect ratio and place the image on a background canvas.
- Recursive folder processing.
- Click-based CLI, tests, type checking, ruff, Sphinx docs, CI, and build targets.

## Installation

```bash
uv sync
```

## Usage

```bash
uv run resizer sample_images output --width 512 --height 512 --mode stretch --overwrite
uv run resizer sample_images output --width 512 --height 512 --mode fit
uv run resizer sample_images output --width 512 --height 512 --mode fill
uv run resizer sample_images output --width 512 --height 512 --mode pad --background 255,255,255
```

## Development

```bash
uv run poe format
uv run poe lint
uv run poe typecheck
uv run poe test
uv run poe docs
uv run poe build
uv run poe standalone
```

## TestPyPI

```bash
uv run python -m build
uv run twine upload --repository testpypi dist/*
```

## Standalone release

```bash
uv run poe standalone
```

Upload `dist/resizer` or `dist/resizer.exe` to GitHub Releases together with source archives.
