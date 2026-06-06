import feedparser
from scrapy.spiders import Spider

from news.items import FeedUrl

with open("news/feeds.txt") as f:
    feeds = [line.strip() for line in f if line.strip()]


class FeedItemSpider(Spider):
    name = "feeds"
    start_urls = feeds

    def parse(self, response):
        page = feedparser.parse(response.body)
        if page.bozo == 0:
            item = FeedUrl()
            item["url"] = response.url
            self.logger.info(response.url)
            return item
