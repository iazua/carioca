"""Public package interface."""

from importlib.metadata import PackageNotFoundError, version

__all__ = ["__version__"]
try:  # gracefully handle execution without installation
    __version__: str = version(__package__ or "carioca")
except PackageNotFoundError:  # pragma: no cover - fallback for tests
    __version__ = "0.0.0"
