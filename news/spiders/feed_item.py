import feedparser
from scrapy.spiders import Spider

from news.items import FeedUrl
from news.seeds import load_seed_lines


class FeedItemSpider(Spider):
    name = "feeds"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = load_seed_lines("feeds.txt")

    def parse(self, response):
        page = feedparser.parse(response.body)
        if page.bozo == 0:
            item = FeedUrl()
            item["url"] = response.url
            self.logger.info(response.url)
            return item
