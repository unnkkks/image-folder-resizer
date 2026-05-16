# Architecture

The package is split into small modules.

- `aspect.py` contains pure calculations for aspect-ratio strategies.
- `image_ops.py` contains Pillow transformations.
- `io.py` contains filesystem traversal and saving.
- `config.py` contains validated user options.
- `cli.py` exposes the Click command.

This separation keeps the image math easy to unit test without touching the filesystem.
