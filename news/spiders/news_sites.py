from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import FeedUrl

with open("news/sites.txt") as f:
    domains = f.readlines()

URLS = [f"http://{domain.strip()}" for domain in domains if "www" in domain]

WWW_URLS = [f"http://www.{domain.strip()}" for domain in domains if "www" not in domain]

URLS.extend(WWW_URLS)


class NewsSiteSpider(CrawlSpider):
    name = "sites"
    allowed_domains = [domain.strip() for domain in domains]
    start_urls = ["http://www.nytimes.com/services/xml/rss/index.html"]  # URLS

    rules = (
        # '.*xml.*', '.*xml.*', '.*rss.*', '.*feed.*', '.*feeds.*'
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
        Rule(LinkExtractor(allow=(r".*",))),
    )

    def parse_item(self, response):
        item = FeedUrl()
        item["url"] = response.url
        self.logger.info(response.url)
        return item
