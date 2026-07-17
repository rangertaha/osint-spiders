"""Shared pytest fixtures and setup.

The spider modules open their seed-list data files (e.g. ``news/news.txt``)
with paths relative to the project root at import time, so make sure the
working directory is the project root before any spider module is imported.
"""

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

os.chdir(PROJECT_ROOT)
