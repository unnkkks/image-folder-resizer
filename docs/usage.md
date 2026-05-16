# Usage examples

## Stretch or compress

```bash
uv run resizer input output --width 640 --height 480 --mode stretch --overwrite
```

Input: any supported folder with `.jpg`, `.png`, `.webp`, `.bmp`, `.gif`, `.tif`, `.tiff` files.

Output: files with exactly `640x480` pixels. Original aspect ratio may change.

## Preserve aspect ratio and fit

```bash
uv run resizer input output --width 640 --height 480 --mode fit
```

A `1000x500` image becomes `640x320`.

## Preserve aspect ratio and crop

```bash
uv run resizer input output --width 640 --height 480 --mode fill
```

The image covers the requested rectangle and is cropped from the center.

## Preserve aspect ratio and pad

```bash
uv run resizer input output --width 640 --height 480 --mode pad --background 255,255,255
```

The image is centered on a `640x480` canvas.
