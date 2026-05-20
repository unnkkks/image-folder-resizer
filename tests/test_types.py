from resizer.types import ResizeMode


def test_resize_mode_values() -> None:
    assert ResizeMode.STRETCH == "stretch"
    assert ResizeMode.KEEP == "keep"
    assert ResizeMode.CROP == "crop"
    assert ResizeMode.PAD == "pad"
