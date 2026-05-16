from resizer.aspect import centered_crop_box, centered_paste_position, fill_size, fit_size


def test_fit_size_preserves_ratio() -> None:
    assert fit_size((100, 50), (50, 50)) == (50, 25)


def test_fill_size_covers_target() -> None:
    assert fill_size((100, 50), (50, 50)) == (100, 50)


def test_centered_crop_box() -> None:
    assert centered_crop_box((100, 60), (50, 40)) == (25, 10, 75, 50)


def test_centered_paste_position() -> None:
    assert centered_paste_position((100, 100), (40, 20)) == (30, 40)
