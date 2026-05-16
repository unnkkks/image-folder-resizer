from resizer.exceptions import (
    InvalidImageError,
    ResizerError,
    UnsupportedFormatError,
)


def test_resizer_error() -> None:
    """Test base exception"""
    assert issubclass(
        ResizerError,
        Exception,
    )


def test_invalid_image_error() -> None:
    """Test invalid image error"""
    assert issubclass(
        InvalidImageError,
        ResizerError,
    )


def test_unsupported_format_error() -> None:
    """Test unsupported format error"""
    assert issubclass(
        UnsupportedFormatError,
        ResizerError,
    )
