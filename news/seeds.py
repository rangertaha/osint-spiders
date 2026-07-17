"""Access to the seed-list data files shipped in ``news/data/``.

The files are resolved through :mod:`importlib.resources`, so loading works
from a source checkout and from an installed wheel alike, regardless of the
current working directory.
"""

from importlib.resources import files


def load_seed_lines(filename: str) -> list[str]:
    """Return the non-empty, stripped lines of ``news/data/<filename>``."""
    text = files("news").joinpath("data", filename).read_text(encoding="utf-8")
    return [line.strip() for line in text.splitlines() if line.strip()]
