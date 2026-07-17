# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `ELASTICSEARCH_URL` setting, consumed by `ElasticsearchPipeline` via
  `from_crawler` (elasticsearch-py 8+ removed the implicit localhost default).
- `RABBITMQ_QUEUE_NAME` setting (default `news_urls`), which `addsites.py`
  has always referenced.
- Offline pytest suite (`tests/`) covering spider parse methods, the
  Elasticsearch pipeline (mocked client), item definitions, settings, and a
  `scrapy list` smoke test.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`): pytest, Ruff, and
  mypy on Python 3.12, 3.13, and 3.14.
- GitHub Actions publish workflow (`.github/workflows/publish.yml`) building
  and publishing to PyPI via Trusted Publishing on release.
- mypy configuration (with overrides for untyped dependencies) and pytest /
  coverage configuration in `pyproject.toml`.
- This changelog.

### Changed

- Require Python >= 3.12.
- Scrapy upgraded to the 2.17 line.
- elasticsearch client upgraded to 9.x.
- `lxml >= 6` forced via a `[tool.uv]` `override-dependencies` entry so the
  project installs on Python 3.14 (temporary until newspaper4k lifts its
  `lxml < 6` cap; `lxml_html_clean` covers the `lxml.html.clean` split).
- Renamed the duplicate spider class names: `feed_urls.NewsFeedSpider` is now
  `FeedUrlSpider` and `news_sites.NewsFeedSpider` is now `NewsSiteSpider`
  (spider names `urls` and `sites` are unchanged).
- Rewrote the README with installation, usage, configuration, and deployment
  documentation.
- `requirements.txt` kept in sync with `pyproject.toml` dependencies.

### Fixed

- `addsites.py` crashed with `AttributeError` because
  `news.settings.RABBITMQ_QUEUE_NAME` did not exist; the setting is now
  defined.
- The `urls` spider (`FeedUrlSpider.parse_item`) yielded duplicate items when
  a response's Content-Type matched more than one entry in `content_types`
  (e.g. `application/xml` matched both `application/xml` and `xml`); it now
  yields at most one item per response.

## [0.1.0] - 2026-06-06

First packaged version.

### Added

- `pyproject.toml` (PEP 621) packaging as the `osint-spiders` distribution,
  version 0.1.0, replacing the empty `setup.py`.
- Ruff configuration.

### Changed

- Cleaned up and modernized the spiders, pipeline, settings, `addsites.py`,
  and `requirements.txt`.

## Initial development (2016-06-15 - 2016-08-14)

The project was originally developed in 2016 without tagged releases; the
notes below are reconstructed from the git history.

- 2016-06-15/16 - repository created; initial Scrapy project (`news`) with a
  feeds spider, Elasticsearch pipeline, items, and settings.
- 2016-06-17 - package restructured to a top-level `news/` package;
  `addsites.py` (RabbitMQ publisher) added.
- 2016-07-29/30 - `feed_urls` spider added; Django-style management commands
  removed; `articles` and `feed_item` spiders added along with seed data
  files (`news.txt`, `feeds.txt`, `terms.txt`); settings and pipeline
  reworked (scrapy-redis scheduler and dupefilter, autothrottle, HTTP cache).
- 2016-08-03 - `news_sites` spider added; sample NYTimes feed list captured.
- 2016-08-13/14 - item, settings, and `feed_urls` spider refinements.

[Unreleased]: https://github.com/Rangertaha/osint-spiders/compare/5775512...HEAD
[0.1.0]: https://github.com/Rangertaha/osint-spiders/commit/5775512
