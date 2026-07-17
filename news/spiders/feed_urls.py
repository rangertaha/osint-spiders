from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import FeedUrl

with open("news/news.txt") as f:
    domains = f.readlines()

URLS = [f"http://{domain.strip()}" for domain in domains if "www" in domain]

WWW_URLS = [f"http://www.{domain.strip()}" for domain in domains if "www" not in domain]

URLS.extend(WWW_URLS)


class FeedUrlSpider(CrawlSpider):
    name = "urls"
    allowed_domains = [domain.strip() for domain in domains]
    start_urls = URLS
    content_types = ["text/xml", "application/xml", "rss", "xml"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(
                    r".*\.xml$",
                    r".*\.atom$",
                    r".*\.rss$",
                    r".*\.feed$",
                    r".*\.feeds$",
                ),
            ),
            callback="parse_item",
        ),
        Rule(
            LinkExtractor(
                allow=(r".*xml.*", r".*rss.*", r".*feed.*", r".*feeds.*"),
            ),
            callback="parse_item",
            follow=True,
        ),
        Rule(LinkExtractor(allow=(r".*",))),
    )

    def parse_item(self, response):
        cts = response.headers.get("Content-Type", b"").decode("latin-1")
        if any(ct in cts for ct in self.content_types):
            self.logger.info(response.url)
            url = FeedUrl()
            url["url"] = response.url
            yield url
