from resizer.exceptions import (
    ResizerError,
    UnsupportedFormatError,
    UnsupportedImageError,
)


def test_resizer_error() -> None:
    """Test base exception."""
    assert issubclass(
        ResizerError,
        Exception,
    )


def test_invalid_image_error() -> None:
    """Test invalid image error."""
    assert issubclass(
        UnsupportedImageError,
        ResizerError,
    )


def test_unsupported_format_error() -> None:
    """Test unsupported format error."""
    assert issubclass(
        UnsupportedFormatError,
        ResizerError,
    )
