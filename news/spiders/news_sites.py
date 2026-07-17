from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from news.items import FeedUrl
from news.seeds import load_seed_lines


class NewsSiteSpider(CrawlSpider):
    name = "sites"
    start_urls = ["http://www.nytimes.com/services/xml/rss/index.html"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.allowed_domains = load_seed_lines("sites.txt")

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
