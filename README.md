# osint-spiders

[![CI](https://github.com/Rangertaha/osint-spiders/actions/workflows/ci.yml/badge.svg)](https://github.com/Rangertaha/osint-spiders/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.12%20%7C%203.13%20%7C%203.14-blue)](https://github.com/Rangertaha/osint-spiders)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

OSINT [Scrapy](https://scrapy.org/) spiders that crawl news sites to discover
RSS/Atom feeds and extract full news articles (via
[newspaper4k](https://github.com/AndyTheFactory/newspaper4k)), storing the
results in Elasticsearch.

## Install

Requires Python >= 3.12. With [uv](https://docs.astral.sh/uv/) (recommended;
required on Python 3.14, see [Known limitations](#known-limitations)):

```sh
git clone https://github.com/Rangertaha/osint-spiders
cd osint-spiders
uv sync
```

Or with pip (Python 3.12/3.13):

```sh
pip install -r requirements.txt
```

## Run

Spiders are run from the project root with `scrapy crawl`:

```sh
uv run scrapy list            # articles, feeds, sites, urls
uv run scrapy crawl articles
```

The scheduler is [scrapy-redis](https://github.com/rmax/scrapy-redis), and
scraped items are indexed into Elasticsearch, so a crawl needs **Redis** and
**Elasticsearch** reachable (see [Configuration](#configuration)).

## Spiders

| Spider     | Class                                    | What it does |
| ---------- | ---------------------------------------- | ------------ |
| `articles` | `news.spiders.articles.ArticleSpider`    | Crawls the domains in `news/news.txt`, extracts full articles with newspaper4k (title, summary, authors, keywords, top image), and yields `Article` items for pieces longer than 1500 characters. |
| `feeds`    | `news.spiders.feed_item.FeedItemSpider`  | Fetches each URL in `news/feeds.txt` and yields a `FeedUrl` item for every URL that parses as a valid feed (feedparser). |
| `urls`     | `news.spiders.feed_urls.FeedUrlSpider`   | Crawls the domains in `news/news.txt` following feed-looking links (`*.xml`, `*.rss`, `*feed*`, ...) and yields a `FeedUrl` item for responses served with an XML/RSS Content-Type. |
| `sites`    | `news.spiders.news_sites.NewsSiteSpider` | Crawls feed index pages (currently seeded with the NYTimes RSS index) and yields `FeedUrl` items for feed links. |

### Seed data files

The spiders read their seed lists at import time from plain-text files in
`news/` (one domain or URL per line), **relative to the project root** — so
always run `scrapy` from the repository root:

| File            | Used by            | Contents |
| --------------- | ------------------ | -------- |
| `news/news.txt` | `articles`, `urls` | News site domains to crawl |
| `news/feeds.txt`| `feeds`            | Candidate feed URLs to validate |
| `news/sites.txt`| `sites`            | News site domains (allowed domains) |
| `news/terms.txt`| (reference)        | Security/OSINT keyword list, not currently read by any spider |
| `news/test.txt` | (reference)        | Small sample domain list for experiments |

## Configuration

Settings live in `news/settings.py`; the interesting ones:

| Setting               | Default                  | Purpose |
| --------------------- | ------------------------ | ------- |
| `ELASTICSEARCH_URL`   | `http://localhost:9200`  | Endpoint used by `ElasticsearchPipeline`, which indexes every item into the `news` index (document id = MD5 of the item URL). |
| `RABBITMQ_QUEUE_NAME` | `news_urls`              | RabbitMQ queue that `addsites.py` publishes raw HTML to for URL extraction. |
| `SCHEDULER` / `DUPEFILTER_CLASS` | scrapy-redis  | Distributed scheduling and dedup through Redis; set `REDIS_URL` (or `REDIS_HOST`/`REDIS_PORT`) to point at your Redis instance (defaults to localhost). |
| `DEPTH_LIMIT`, `DOWNLOAD_DELAY`, `AUTOTHROTTLE_*`, `HTTPCACHE_*` | see file | Crawl politeness and caching knobs. |

Any setting can be overridden per run: `scrapy crawl articles -s ELASTICSEARCH_URL=http://es:9200`.

### addsites.py

`addsites.py` is a small standalone helper that publishes raw HTML to the
RabbitMQ queue named by `RABBITMQ_QUEUE_NAME` (broker on `localhost`) for
downstream URL extraction. It is not part of the Scrapy crawl.

## Deploying to Scrapyd

`scrapy.cfg` contains a `[deploy]` section with the project name `news`, but
the Scrapyd `url` is commented out — deployment is not wired to any live
server. To use it, run a [Scrapyd](https://scrapyd.readthedocs.io/) instance,
uncomment/point `url` at it, and deploy with
[scrapyd-client](https://github.com/scrapy/scrapyd-client):

```sh
scrapyd-deploy default -p news
```

## Development

```sh
uv sync --group dev
uv run pytest --cov=news   # offline test suite
uvx ruff format --check .  # formatting
uvx ruff check .           # lint
uv run mypy                # type check
```

All tests are offline: no live sites, Elasticsearch, Redis, or RabbitMQ are
contacted.

## Known limitations

- **Seed files are cwd-relative and not packaged.** Spider modules `open()`
  their `.txt` seed lists at import time relative to the current working
  directory, and the files are not included in the wheel/sdist. Running from
  the repository root works; running an installed distribution does not.
  Moving the reads to `start_requests()` with `importlib.resources` (and
  declaring the files as package data) is the planned fix.
- **lxml override.** newspaper4k currently pins `lxml < 6`, but only
  `lxml >= 6.0.1` ships CPython 3.14 wheels. The `[tool.uv]`
  `override-dependencies` entry in `pyproject.toml` forces `lxml >= 6.0.1`
  (safe because `lxml_html_clean` provides the split-out `lxml.html.clean`).
  Remove it once newspaper4k lifts the cap. Plain-pip installs therefore only
  work on Python 3.12/3.13.

## License

[MIT](LICENSE)
