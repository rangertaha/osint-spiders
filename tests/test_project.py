"""Smoke tests for the Scrapy project as a whole (offline)."""

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EXPECTED_SPIDERS = {"articles", "feeds", "sites", "urls"}


def test_scrapy_list_names_all_spiders():
    result = subprocess.run(
        [sys.executable, "-m", "scrapy", "list"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert set(result.stdout.split()) == EXPECTED_SPIDERS


def test_spider_loader_finds_all_spiders():
    from scrapy.spiderloader import SpiderLoader
    from scrapy.utils.project import get_project_settings

    settings = get_project_settings()
    loader = SpiderLoader.from_settings(settings)
    assert set(loader.list()) == EXPECTED_SPIDERS
