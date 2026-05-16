"""Custom exceptions for the resizer package."""


class ResizerError(Exception):
    """Base exception for image-folder-resizer."""


class UnsupportedImageError(ResizerError):
    """Raised when a file cannot be opened as an image."""


class OutputExistsError(ResizerError):
    """Raised when output exists and overwriting is disabled."""
