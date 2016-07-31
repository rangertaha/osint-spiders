import time
import scrapy
from scrapy.spiders import CrawlSpider, Rule, BaseSpider, Spider
from scrapy.linkextractors import LinkExtractor
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import feedparser
import newspaper

from news.items import FeedUrl

with open('news/feeds.txt') as f:
    feeds = f.readlines()


class FeedItemSpider(Spider):
    name = 'feeds'
    start_urls = feeds

    def parse(self, response):
        page = feedparser.parse(response.body)
        if page.bozo == 0:
            item = FeedUrl()
            item['url'] = response.url
            print response.url
            return item

