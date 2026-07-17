from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import FeedUrl
from news.seeds import load_seed_lines


class FeedUrlSpider(CrawlSpider):
    name = "urls"
    content_types = ["text/xml", "application/xml", "rss", "xml"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        domains = load_seed_lines("news.txt")
        self.allowed_domains = domains
        urls = [f"http://{domain}" for domain in domains if "www" in domain]
        urls.extend(f"http://www.{domain}" for domain in domains if "www" not in domain)
        self.start_urls = urls

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
